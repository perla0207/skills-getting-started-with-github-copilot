Plan: Participant management feature

1. Add participants UI to `src/static/app.js`
   - Render a "Participants" section in each activity card
   - Display participants as a bulleted list (or "None yet" when empty)
   - Add a remove icon/button next to each participant
   - Reset the activity select to avoid duplicate options on reload

2. Style participants list in `src/static/styles.css`
   - Hide native bullets and display a clean list
   - Style remove icon (hover state, accessible color)
   - Make the section visually separated (dashed top border, spacing)

3. Add backend DELETE endpoint in `src/app.py`
   - New endpoint: `DELETE /activities/{activity_name}/participants?email=...`
   - Validate activity exists; return 404 if not
   - Validate participant exists; return 404 if not
   - Remove participant and return success message

4. Wire delete buttons in `src/static/app.js` to call DELETE
   - Use event delegation on the activities list container
   - Confirm with the user before deleting
   - Show success/error message and refresh activities list on change

5. Refresh UI after signup
   - Call `fetchActivities()` after successful POST signup so new participants appear without page reload

6. Tests: add pytest tests under `tests/`
   - Create `tests/test_app.py` using `TestClient(app)`
   - Fixture to deepcopy and restore in-memory `activities` between tests
   - Tests for: GET /activities, POST signup (success + duplicate), DELETE participant (success + not found), activity not found errors

7. Verification and polish
   - Run server locally: `uvicorn src.app:app --reload` and manually verify flows
   - Run tests: `pytest -q`
   - Consider sorting participants alphabetically and collapsing long lists with a "show more" toggle as follow-ups
