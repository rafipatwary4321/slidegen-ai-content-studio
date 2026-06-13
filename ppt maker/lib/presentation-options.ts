/**
 * Canonical persona and theme values (API + UI). Not sample data — these match backend literals.
 */
export const PERSONAS = ["Student", "Business", "Marketing", "Corporate"] as const;
export const THEMES = ["Cinematic Dark", "Professional Light"] as const;

export type PersonaOption = (typeof PERSONAS)[number];
export type ThemeOption = (typeof THEMES)[number];
