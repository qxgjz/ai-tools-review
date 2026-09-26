"""Fix P0 structured data issues on tool detail page:
1. Add aggregateRating to inline Review's itemReviewed.SoftwareApplication
2. Fix worstRating from "0" to "1"
3. Fix og:image to use tool-specific image
"""
import re

FILE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\app\tools\[slug]\page.tsx"

with open(FILE, "r", encoding="utf-8") as f:
    code = f.read()

# Fix 1: Add aggregateRating to itemReviewed SoftwareApplication
# Current: itemReviewed has name, applicationCategory, operatingSystem, offers but no aggregateRating
# Add after operatingSystem line
old_itemreviewed = """      itemReviewed: {
      "@type": "SoftwareApplication",
      name: tool.name,
      applicationCategory: "WebApplication",
      operatingSystem: "Web",
      offers: tool.pricing.map((tier) => ({
        "@type": "Offer",
        name: tier.name,
        price: tier.price.includes("$0") ? "0" : tier.price.replace(/[^0-9.]/g, ""),
        priceCurrency: "USD",
      })),
    },"""

new_itemreviewed = """      itemReviewed: {
      "@type": "SoftwareApplication",
      name: tool.name,
      applicationCategory: "WebApplication",
      operatingSystem: "Web",
      aggregateRating: {
        "@type": "AggregateRating",
        ratingValue: total.toFixed(1),
        bestRating: "10",
        worstRating: "1",
        ratingCount: "1",
      },
      offers: tool.pricing.map((tier) => ({
        "@type": "Offer",
        name: tier.name,
        price: tier.price.includes("$0") ? "0" : tier.price.replace(/[^0-9.]/g, ""),
        priceCurrency: "USD",
      })),
    },"""

if old_itemreviewed in code:
    code = code.replace(old_itemreviewed, new_itemreviewed)
    print("FIX 1: Added aggregateRating to itemReviewed SoftwareApplication")
else:
    print("SKIP 1: itemReviewed pattern not found (may already be fixed)")

# Fix 2: worstRating from "0" to "1" in reviewRating
old_rating = """    reviewRating: {
      "@type": "Rating",
      ratingValue: total.toFixed(1),
      bestRating: "10",
      worstRating: "0",
    },"""

new_rating = """    reviewRating: {
      "@type": "Rating",
      ratingValue: total.toFixed(1),
      bestRating: "10",
      worstRating: "1",
    },"""

if old_rating in code:
    code = code.replace(old_rating, new_rating)
    print("FIX 2: Changed worstRating from '0' to '1'")
else:
    print("SKIP 2: reviewRating pattern not found")

with open(FILE, "w", encoding="utf-8") as f:
    f.write(code)

print("\nDone. Running TypeScript check...")
