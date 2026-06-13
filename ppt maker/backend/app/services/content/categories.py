"""Category metadata shared across content generation handlers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CategorySpec:
    id: str
    name: str
    default_aspect: str
    exports: tuple[str, ...]
    system_hint: str


CATEGORY_SPECS: dict[str, CategorySpec] = {
    "presentations": CategorySpec(
        id="presentations",
        name="Presentations",
        default_aspect="16:9",
        exports=("pptx", "pdf", "png", "zip"),
        system_hint="Slide deck with title, agenda, key points, data, conclusion.",
    ),
    "news-photocards": CategorySpec(
        id="news-photocards",
        name="News Photocards",
        default_aspect="4:5",
        exports=("png", "jpg", "pdf"),
        system_hint="Editorial news photocard with headline, subhead, image area, source line.",
    ),
    "breaking-news-cards": CategorySpec(
        id="breaking-news-cards",
        name="Breaking News Cards",
        default_aspect="16:9",
        exports=("png", "jpg"),
        system_hint="Urgent breaking news banner with bold alert strip and headline.",
    ),
    "event-posters": CategorySpec(
        id="event-posters",
        name="Event Posters",
        default_aspect="A4",
        exports=("png", "pdf"),
        system_hint="Event poster with title, date, venue, CTA.",
    ),
    "facebook-posts": CategorySpec("facebook-posts", "Facebook Posts", "1:1", ("png", "jpg"), "Social feed post with hook and CTA."),
    "instagram-posts": CategorySpec("instagram-posts", "Instagram Posts", "1:1", ("png", "jpg"), "Instagram feed creative with bold headline."),
    "instagram-stories": CategorySpec("instagram-stories", "Instagram Stories", "9:16", ("png", "jpg"), "Vertical story with swipe-up CTA."),
    "facebook-covers": CategorySpec("facebook-covers", "Facebook Covers", "16:9", ("png", "jpg"), "Page cover with safe crop zones."),
    "youtube-thumbnails": CategorySpec("youtube-thumbnails", "YouTube Thumbnails", "16:9", ("png", "jpg"), "High-contrast thumbnail with face/text zones."),
    "youtube-community-posts": CategorySpec("youtube-community-posts", "YouTube Community", "1:1", ("png", "jpg"), "Community announcement card."),
    "political-posters": CategorySpec("political-posters", "Political Posters", "A4", ("png", "pdf"), "Campaign poster with slogan and candidate block."),
    "educational-posters": CategorySpec("educational-posters", "Educational Posters", "A4", ("png", "pdf"), "Classroom poster with learning objectives."),
    "certificates": CategorySpec("certificates", "Certificates", "A4", ("png", "pdf"), "Award certificate with recipient and signature lines."),
    "id-cards": CategorySpec("id-cards", "ID Cards", "16:9", ("png", "pdf"), "ID card with photo placeholder and fields."),
    "flyers": CategorySpec("flyers", "Flyers", "A4", ("png", "pdf", "jpg"), "Promotional flyer with offer and contact."),
    "brochures": CategorySpec("brochures", "Brochures", "A4", ("pdf", "png"), "Tri-fold brochure panels."),
    "infographics": CategorySpec("infographics", "Infographics", "4:5", ("png", "pdf"), "Data infographic with sections and chart placeholders."),
    "resume-builder": CategorySpec("resume-builder", "Resume", "A4", ("pdf", "png"), "Professional resume sections."),
    "invitation-cards": CategorySpec("invitation-cards", "Invitations", "4:5", ("png", "pdf"), "Event invitation with RSVP."),
    "ad-creatives": CategorySpec("ad-creatives", "Ad Creatives", "1:1", ("png", "jpg", "zip"), "Performance ad with headline and product focus."),
    "product-promotions": CategorySpec("product-promotions", "Product Promos", "1:1", ("png", "jpg"), "Product launch promo layout."),
    "ngo-campaign-materials": CategorySpec("ngo-campaign-materials", "NGO Campaigns", "4:5", ("png", "pdf"), "Awareness campaign visual."),
    "real-estate-templates": CategorySpec("real-estate-templates", "Real Estate", "16:9", ("png", "pdf"), "Property listing card."),
    "restaurant-marketing": CategorySpec("restaurant-marketing", "Restaurant", "1:1", ("png", "jpg"), "Menu promo or dish highlight."),
    "podcast-covers": CategorySpec("podcast-covers", "Podcast Covers", "1:1", ("png", "jpg"), "Podcast cover art square."),
    "poster-generator": CategorySpec(
        "poster-generator",
        "Poster Generator",
        "A4",
        ("png", "pdf", "jpg"),
        "Marketing poster with title, subtitle, date, venue, organizer, and CTA.",
    ),
}


def get_category_spec(category_id: str) -> CategorySpec:
    return CATEGORY_SPECS.get(category_id) or CategorySpec(
        category_id,
        category_id.replace("-", " ").title(),
        "16:9",
        ("png", "pdf"),
        "General marketing design.",
    )
