class BookingSummary {
  const BookingSummary({
    required this.bookingId,
    required this.status,
    required this.digitalKey,
    required this.listingTitle,
    required this.listingLatitude,
    required this.listingLongitude,
    required this.agreementDocumentUrl,
    required this.checkIn,
    required this.checkOut,
    required this.totalAmount,
  });

  final int bookingId;
  final String status;
  final String? digitalKey;
  final String listingTitle;
  final double listingLatitude;
  final double listingLongitude;
  final String? agreementDocumentUrl;
  final String checkIn;
  final String checkOut;
  final String totalAmount;

  factory BookingSummary.fromJson(Map<String, dynamic> json) {
    return BookingSummary(
      bookingId: (json['booking_id'] as num).toInt(),
      status: json['status'] as String,
      digitalKey: json['digital_key'] as String?,
      listingTitle: json['listing_title'] as String,
      listingLatitude: (json['listing_latitude'] as num).toDouble(),
      listingLongitude: (json['listing_longitude'] as num).toDouble(),
      agreementDocumentUrl: json['agreement_document_url'] as String?,
      checkIn: json['check_in'] as String,
      checkOut: json['check_out'] as String,
      totalAmount: json['total_amount'].toString(),
    );
  }
}
