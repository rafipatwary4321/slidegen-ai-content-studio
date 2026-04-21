import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import '../models/app_user.dart';
import '../services/auth_api.dart';
import '../services/session_notifier.dart';
import '../services/session_store.dart';
import '../services/users_api.dart';

class AccountScreen extends StatefulWidget {
  const AccountScreen({super.key});

  @override
  State<AccountScreen> createState() => _AccountScreenState();
}

class _AccountScreenState extends State<AccountScreen> {
  int? _userId;
  final _nameCtrl = TextEditingController();
  final _phoneCtrl = TextEditingController();
  final _emailCtrl = TextEditingController();
  String _role = 'Guest';
  bool _busy = false;
  String? _lastNidStatus;

  @override
  void initState() {
    super.initState();
    _load();
  }

  @override
  void dispose() {
    _nameCtrl.dispose();
    _phoneCtrl.dispose();
    _emailCtrl.dispose();
    super.dispose();
  }

  Future<void> _load() async {
    final id = await SessionStore.getUserId();
    if (mounted) setState(() => _userId = id);
  }

  Future<void> _register() async {
    final name = _nameCtrl.text.trim();
    final phone = _phoneCtrl.text.trim();
    final email = _emailCtrl.text.trim();
    if (name.isEmpty || phone.isEmpty || email.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Fill name, phone, and email')),
      );
      return;
    }
    setState(() => _busy = true);
    try {
      final AppUser u = await createUser(
        fullName: name,
        phone: phone,
        email: email,
        role: _role,
      );
      await SessionStore.setUserId(u.id);
      SessionNotifier.instance.notifySessionChanged();
      if (mounted) {
        setState(() {
          _userId = u.id;
          _busy = false;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Signed in as ${u.fullName} (#${u.id})')),
        );
      }
    } on UsersApiException catch (e) {
      if (mounted) {
        setState(() => _busy = false);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(e.message)),
        );
      }
    } catch (e) {
      if (mounted) {
        setState(() => _busy = false);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('$e')),
        );
      }
    }
  }

  Future<void> _signOut() async {
    await SessionStore.clearUserId();
    SessionNotifier.instance.notifySessionChanged();
    if (mounted) {
      setState(() {
        _userId = null;
        _lastNidStatus = null;
      });
    }
  }

  Future<void> _uploadNid() async {
    final uid = _userId;
    if (uid == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Register first to attach NID to your user.')),
      );
      return;
    }
    final picker = ImagePicker();
    final x = await picker.pickImage(
      source: ImageSource.gallery,
      maxWidth: 2000,
      imageQuality: 85,
    );
    if (x == null) return;
    final bytes = await x.readAsBytes();
    if (bytes.isEmpty) return;

    setState(() => _busy = true);
    try {
      final res = await verifyNid(
        userId: uid,
        fileBytes: Uint8List.fromList(bytes),
        filename: x.name,
      );
      if (mounted) {
        setState(() {
          _busy = false;
          _lastNidStatus = res['status']?.toString() ?? 'Submitted';
        });
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'NID: ${res['status']} · n8n: ${res['n8n_dispatched']}',
            ),
          ),
        );
      }
    } on AuthApiException catch (e) {
      if (mounted) {
        setState(() => _busy = false);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(e.message)),
        );
      }
    } catch (e) {
      if (mounted) {
        setState(() => _busy = false);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('$e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Account')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          if (_userId != null)
            Card(
              child: ListTile(
                leading: const CircleAvatar(child: Icon(Icons.person)),
                title: Text('User #$_userId'),
                subtitle: const Text('Used for bookings & Bachelor match on map'),
                trailing: TextButton(
                  onPressed: _busy ? null : _signOut,
                  child: const Text('Sign out'),
                ),
              ),
            )
          else
            Text(
              'Create a guest account to book stays and improve map matching.',
              style: theme.textTheme.bodyMedium?.copyWith(
                color: theme.colorScheme.onSurfaceVariant,
              ),
            ),
          const SizedBox(height: 20),
          TextField(
            controller: _nameCtrl,
            decoration: const InputDecoration(
              labelText: 'Full name',
              border: OutlineInputBorder(),
            ),
            textCapitalization: TextCapitalization.words,
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _phoneCtrl,
            decoration: const InputDecoration(
              labelText: 'Phone',
              border: OutlineInputBorder(),
            ),
            keyboardType: TextInputType.phone,
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _emailCtrl,
            decoration: const InputDecoration(
              labelText: 'Email',
              border: OutlineInputBorder(),
            ),
            keyboardType: TextInputType.emailAddress,
          ),
          const SizedBox(height: 12),
          DropdownButtonFormField<String>(
            value: _role,
            decoration: const InputDecoration(
              labelText: 'Role',
              border: OutlineInputBorder(),
            ),
            items: const [
              DropdownMenuItem(value: 'Guest', child: Text('Guest')),
              DropdownMenuItem(value: 'Host', child: Text('Host')),
            ],
            onChanged: _busy ? null : (v) => setState(() => _role = v ?? 'Guest'),
          ),
          const SizedBox(height: 20),
          FilledButton(
            onPressed: _busy ? null : _register,
            child: _busy
                ? const SizedBox(
                    width: 22,
                    height: 22,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : Text(_userId == null ? 'Register / save profile' : 'Update (new user)'),
          ),
          const SizedBox(height: 32),
          Text(
            'NID verification',
            style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600),
          ),
          const SizedBox(height: 8),
          Text(
            'Uploads to the API and forwards to n8n when configured.',
            style: theme.textTheme.bodySmall?.copyWith(
              color: theme.colorScheme.onSurfaceVariant,
            ),
          ),
          const SizedBox(height: 12),
          OutlinedButton.icon(
            onPressed: _busy ? null : _uploadNid,
            icon: const Icon(Icons.badge_outlined),
            label: const Text('Upload NID image'),
          ),
          if (_lastNidStatus != null)
            Padding(
              padding: const EdgeInsets.only(top: 12),
              child: Text('Last: $_lastNidStatus'),
            ),
        ],
      ),
    );
  }
}
