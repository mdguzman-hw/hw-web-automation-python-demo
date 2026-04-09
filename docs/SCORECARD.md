# Codebase Scorecard — web-automation-demo

---

## Score

| | |
|---|---|
| **Previous** | 7 / 10 |
| **Current** | 7.5 / 10 |
| **Last reviewed** | 2026-04-09 |

---

## What Improved

| # | Item | Previous | Status |
|---|------|----------|--------|
| 1 | Loading spinner consistency — `loadingPage` invisibility now in all `wait_for_*` methods | Missing from 8 methods | **Fixed** |
| 2 | `is_assessment_complete()` BETA URL pattern — now checks both `pathfinder/assessment` and `recommendation` independently | Would never match BETA URL | **Fixed** |
| 3 | XPath in `continue_booking` — `/p` → `//p` | Silent DOM mismatch | **Fixed** |
| 4 | `wait_for_booking_create` — added `loadingPage` wait and env-specific container (`container-confirm-booking` for BETA) | Wrong container, no spinner wait | **Fixed** |
| 5 | `navigate_toc` intermittent failure — pre-checks `program_status_endpoint` before attempting click | Stale element race condition | **Fixed (workaround)** |
| 6 | Meet Now speedbump in `complete_service_confirm_form` — waits for either `meetnow` or `booking` URL | Missing speedbump path caused timeout | **Fixed** |
| 7 | `InsecureRequestWarning` suppressed via `pytest.ini filterwarnings` | Polluted test output | **Fixed** |
| 8 | Duplicate `test_bat_web_006` function name | Silent test loss | **Fixed** |
| 9 | `test_smoke_homeweb_006` implemented — PulseCheck slider for all 5 feelings with history validation | Stubbed / skipped | **Implemented** |
| 10 | `wait_for_booking_details` — detects `section-error`, prints error text, and skips test cleanly | Would timeout and fail | **Fixed** |
| 11 | `PulseCheck` class extracted — constants live at module level alongside `DashboardTile`, `ProviderTile` | N/A | **New** |
| 12 | Wellness nav added to `HeaderHomeweb` EN/FR (`navigate_wellness()`) | Missing | **New** |
| 13 | `navigate_pulsecheck()` added — navigates via dashboard tile, used in smoke_005 and smoke_006 loop | Inline in test | **Refactored** |

---

## Open Issues

| # | Issue | Severity | Notes |
|---|-------|----------|-------|
| 1 | **`PulseCheck.LABELS` English-only** | Medium | `get_latest_pulsecheck_history()` returns DOM text (localized), but `LABELS` only has English. The history validation in `test_smoke_homeweb_006` will fail in a FR session. TODO comment added in smoke_017 for related aria-label issue. |
| 2 | **Duplicate `wait_for_resources` definition** | Low | First definition is dead code, silently overridden by the second. Still unremoved. |
| 3 | **Env branching expanding inside page objects** | Medium | `if self.env == "beta"` now spans: `confirm_booking`, `select_booking_options`, `wait_for_booking_create`, `wait_for_booking_digest`, `wait_for_booking_details`, `complete_service_confirm_form`, `ProviderTile.provider_details_link`. Each new BETA divergence adds to this debt. |
| 4 | **Unreachable `return True` in `wait_for_booking_details`** | Low | Live `return True` followed by a commented-out block with another unreachable `return True`. Dead code that reads as if it executes. |
| 5 | **`time.sleep()` workarounds** | Medium | Still present in: `navigate_overview`, `start_program`, `continue_goal` (SentioClient); `end_services`, `select_provider` (Homeweb); `DashboardTile.navigate`. None replaced with `wait.until` conditions. |
| 6 | **`BasePage.click_element` double DOM lookup** | Medium | Root issue unresolved — two separate `wait.until` calls for the same element create a stale-element window. Currently worked around in `navigate_toc` and triggered in `navigate_wellness`. |
| 7 | **`phone` variable reused for comments field** | Low | `complete_booking_create_form`: `phone = self.wait.until(...(By.ID, "comments"))`. Misleading variable name. |
| 8 | **Dead and commented-out code** | Low | Spread across both files: alternative XPaths, old `wait_for_resources` variant, incomplete `select_provider_time`, `choose_confirmation_method` stub, debug `print` statements, stale TODO comments. |
| 9 | **`pre_url` dead variable in `wait_for_next_step`** | Low | `pre_url = self.current_url` is assigned on entry but never read. |
| 10 | **`SentioClient.__init__` env branch is inert** | Low | Both `if env == "prod"` and `else` branches assign the same `SENTIO_BETA_CLIENT_*` constants. The conditional does nothing. |

---

## Recommendations

| Priority | Action |
|----------|--------|
| High | Fix `BasePage.click_element` — single `wait.until(element_to_be_clickable)` call to eliminate the stale-element window |
| High | Add `PulseCheck.LABELS` FR entries — confirm French feeling label text and make history validation language-aware |
| Medium | Replace `time.sleep()` with `wait.until` conditions in `select_provider`, `end_services`, `DashboardTile.navigate`, and SentioClient scroll methods |
| Medium | Evaluate BETA subclass or strategy to stop `if self.env` branching from growing further in page methods |
| Low | Remove first `wait_for_resources` definition |
| Low | Remove `pre_url` dead variable from `wait_for_next_step` |
| Low | Fix or remove `SentioClient.__init__` env conditional — assign correct PROD constants or remove the branch |
| Low | Rename `phone` → `comments` in `complete_booking_create_form` |
| Low | Audit and remove all commented-out code, stale TODOs, and debug `print` statements |
