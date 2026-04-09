# Codebase Scorecard — web-automation-demo

---

## Score

| | |
|---|---|
| **Previous** | 6 / 10 |
| **Current** | 7 / 10 |
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

---

## Open Issues

| # | Issue | Severity | Notes |
|---|-------|----------|-------|
| 1 | **Duplicate `wait_for_resources` definition** | Low | First definition (lines 62–70) is dead code, silently overridden by the second. Still unremoved. |
| 2 | **Env branching expanding inside page objects** | Medium | `if self.env == "beta"` has grown to: `confirm_booking`, `select_booking_options`, `wait_for_booking_create`, `wait_for_booking_digest`, `wait_for_booking_details`, `complete_service_confirm_form`, and `ProviderTile.provider_details_link`. Each new BETA divergence adds to this debt. |
| 3 | **Unreachable `return True` in `wait_for_booking_details`** | Low | Live `return True` at line 312, then a commented-out block with another `return True` at line 330. Dead code that reads as if it executes. |
| 4 | **`time.sleep()` workarounds** | Medium | Still present in: `navigate_overview`, `start_program`, `continue_goal` (SentioClient); `end_services`, `select_provider` (Homeweb); `DashboardTile.navigate`. None replaced with `wait.until` conditions. |
| 5 | **`BasePage.click_element` double DOM lookup** | Medium | Root issue unresolved in BasePage — two separate `wait.until` calls for the same element create a stale-element window. Currently worked around in `navigate_toc`, but any other method using `click_element` on dynamic elements is still exposed. |
| 6 | **`phone` variable reused for comments field** | Low | `complete_booking_create_form` line 820: `phone = self.wait.until(...(By.ID, "comments"))`. Misleading variable name. |
| 7 | **Dead and commented-out code** | Low | Spread across both files: alternative XPaths, old `wait_for_resources` variant, incomplete `select_provider_time`, `choose_confirmation_method` stub, debug `print` statements, stale TODO comments. |
| 8 | **`pre_url` dead variable in `wait_for_next_step`** | Low | `pre_url = self.current_url` is assigned on entry but never read. |
| 9 | **`SentioClient.__init__` env branch is inert** | Low | Both `if env == "prod"` and `else` branches assign the same `SENTIO_BETA_CLIENT_*` constants. The conditional does nothing. |

---

## Recommendations

| Priority | Action |
|----------|--------|
| High | Fix `BasePage.click_element` — single `wait.until(element_to_be_clickable)` call to eliminate the stale-element window |
| Medium | Replace `time.sleep()` with `wait.until` conditions in `select_provider`, `end_services`, `DashboardTile.navigate`, and SentioClient scroll methods |
| Medium | Evaluate BETA subclass or strategy to stop `if self.env` branching from growing further in page methods |
| Low | Remove first `wait_for_resources` definition |
| Low | Remove `pre_url` dead variable from `wait_for_next_step` |
| Low | Fix or remove `SentioClient.__init__` env conditional — assign correct PROD constants or remove the branch |
| Low | Rename `phone` → `comments` in `complete_booking_create_form` |
| Low | Audit and remove all commented-out code, stale TODOs, and debug `print` statements |
