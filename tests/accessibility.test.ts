import { describe, it, expect } from "vitest";
import axe from "axe-core";

/**
 * Accessibility unit tests using axe-core
 * These test utility functions for a11y compliance.
 * E2E axe-core tests run in Playwright (see P1-QA-PLAYWRIGHT-001).
 */
describe("Accessibility utilities", () => {
  it("axe-core should be configured", () => {
    expect(axe).toBeDefined();
    expect(typeof axe.run).toBe("function");
  });

  it("should validate WCAG 2.2 AA tag exists", () => {
    const tags = axe.getRules(["wcag2a", "wcag2aa", "wcag22aa"]);
    expect(tags.length).toBeGreaterThan(0);
  });
});
