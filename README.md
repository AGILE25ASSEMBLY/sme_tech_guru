# SME Tech Guru

**SME Tech Guru** is a Streamlit web application that helps students and project teams discover faculty subject-matter experts for research, academic projects, mentoring, and idea development.

The application combines a Google Sheets-based faculty registration source with a locally cached Pandas data file. It provides search and filtering controls, groups matching faculty by department, and renders their names, specializations, experience, research output, teaching status, and Google Scholar profile links.

> Brand shown in the application: **SME Tech Guru**
>
> Organization shown in the application: **Agile Assembly**, "A Prince Campus Company"

## Table of Contents

- [What the application does](#what-the-application-does)
- [Feature overview](#feature-overview)
- [User journey](#user-journey)
- [Application architecture](#application-architecture)
- [Data flow](#data-flow)
- [Data model](#data-model)
- [Repository structure](#repository-structure)
- [Installation](#installation)
- [Running the application](#running-the-application)
- [Refreshing faculty data](#refreshing-faculty-data)
- [Google Sheets configuration](#google-sheets-configuration)
- [Filtering behavior](#filtering-behavior)
- [UI and theming](#ui-and-theming)
- [Error handling](#error-handling)
- [Deployment](#deployment)
- [Security and privacy](#security-and-privacy)
- [Limitations](#limitations)
- [Troubleshooting](#troubleshooting)
- [Maintainer guide](#maintainer-guide)

## What the application does

SME Tech Guru acts as a searchable faculty expertise directory.

From an end-user perspective, it allows a visitor to:

1. Open the application in a browser.
2. Filter faculty by one or more areas of specialization.
3. Choose whether to include only faculty currently teaching the relevant subject.
4. Search for a faculty member by name.
5. Review matching faculty grouped by department.
6. Open a faculty member's Google Scholar profile in a new browser tab.

From a technical perspective, it consists of:

- A data-preparation script that downloads a Google Sheets CSV export and normalizes it.
- A cached Pandas/Streamlit application that loads the normalized file and provides the search interface.
- A binary `faculty_data.pkl` file that is the runtime source of faculty records.
- A Streamlit theme configuration for consistent colors and typography.

## Feature overview

### 1. Faculty specialization discovery

The application reads the `specialization` value for every faculty row, splits comma-separated values, removes surrounding whitespace and empty entries, removes duplicates, and displays the result in a sorted multi-select control.

Example:

```text
"Machine Learning, Data Science"
"Artificial Intelligence, Machine Learning"
```

produces individual filter choices similar to:

```text
Artificial Intelligence
Data Science
Machine Learning
```

The options are generated dynamically, so new specializations from the source sheet appear after the data is refreshed.

### 2. Multi-specialization filtering

Users can select one or more specialization values. A row matches if **any selected specialization appears anywhere inside that faculty member's specialization text**.

The comparison is case-insensitive. For example, selecting `Machine Learning` matches a specialization string such as `Machine Learning and Deep Learning`.

### 3. "Currently teaching" filter

A checkbox, enabled by default, filters out faculty whose `currently_teaching` value is not `Yes`.

This feature is intended to prioritize faculty who are actively teaching in the selected area. Users can disable the checkbox to include both actively teaching faculty and faculty who are not currently teaching that subject.

### 4. Faculty name search

The name search is a free-text, case-insensitive substring search over `faculty_name`.

Example: searching for `ra` may match `Prashant`, `Ramesh`, and `Rahul`, depending on the records in the dataset.

The search and all selected filters are combined. This means the final result must satisfy all active criteria.

### 5. Department-based results

Filtered results are grouped by `department`. Departments are discovered from the filtered data and sorted alphabetically. Each department is shown under a dedicated heading.

For each department, the application displays:

- Faculty name
- Specialization
- Research papers
- Experience
- Whether the faculty member is currently teaching
- Google Scholar link

Only mapped columns that exist in the dataframe are displayed.

### 6. Clickable Google Scholar profiles

Google Scholar URLs are converted into an HTML link labeled **View Profile**.

Behavior:

- `https://...` and `http://...` URLs are preserved.
- URLs without a recognized scheme receive `http://` automatically.
- Missing, empty, or non-string values display `N/A`.

Links open in a new browser tab.

### 7. Clear result summary and empty-state feedback

After filtering, the application reports the number of matching faculty. If no records match, it displays a user-friendly empty-state message asking the user to broaden or adjust the search.

### 8. Cached data loading

`load_faculty_data()` is decorated with `@st.cache_data(ttl=3600)`, which caches faculty loading and specialization extraction for up to one hour.

This reduces repeated file reads and processing while the Streamlit session and process remain active.

### 9. Branded, responsive presentation

The application presents:

- Prince Campus Company attribution
- Agile Assembly attribution
- The SME Tech Guru title
- A motivational subtitle
- A welcome message
- Styled section headings
- A wide Streamlit layout
- A collapsed initial sidebar
- Custom table and container styling
- Streamlit menu/footer suppression

## User journey

```text
Visitor
  |
  | 1. Opens the Streamlit application
  v
Faculty directory loads from faculty_data.pkl
  |
  | 2. Specializations are split and made available in a multi-select
  v
Visitor selects specialization(s)
  |
  | 3. Optionally enables "currently teaching"
  | 4. Optionally enters a name
  v
Application combines the filters
  |
  v
Results are grouped by department
  |
  v
Visitor opens a Google Scholar profile when relevant
```

## Application architecture

The repository uses a small, script-oriented architecture:

```text
+-----------------------+
| Google Sheet (CSV)    |
+----------+------------+
           |
           | Public CSV export
           v
+-----------------------+
| 01_prepare_data.py    |
| - Download            |
| - Rename columns      |
| - Normalize values    |
| - Validate required   |
| - Serialize           |
+----------+------------+
           |
           | Pandas pickle
           v
+-----------------------+
| faculty_data.pkl      |
+----------+------------+
           |
           | Cached read
           v
+-----------------------+
| SME_Tech_Guru.py      |
| - Load data           |
| - Extract filters     |
| - Apply filters       |
| - Group by department |
| - Render HTML/UI      |
+----------+------------+
           |
           | Streamlit browser UI
           v
+-----------------------+
| Visitor / browser     |
+-----------------------+
```

### Main application entry point

`SME_Tech_Guru.py` is the Streamlit entry point:

- Configures the page.
- Defines global constants and theme CSS.
- Loads and caches faculty data.
- Builds search controls.
- Applies the filters.
- Groups and renders results.
- Calls `main()` when the script is executed directly.

### Data preparation entry point

`01_prepare_data.py` is the offline/maintenance entry point:

- Constructs a CSV export URL from the configured Google Sheets URL.
- Reads the sheet with `pandas.read_csv()`.
- Removes the `Timestamp` column when present.
- Standardizes source column names.
- Normalizes `currently_teaching`.
- Validates the required columns.
- Saves the resulting dataframe to `faculty_data.pkl`.
- Prints a short processing summary and the first five processed rows.

## Data flow

### Refresh flow

1. A faculty/staff member enters or updates data in the Google Sheet.
2. The maintainer runs `python 01_prepare_data.py`.
3. The script creates a public CSV export URL from the Google Sheets document ID.
4. Pandas downloads and parses the CSV.
5. Source headers are cleaned and mapped to stable application names.
6. `currently_teaching` is normalized to `Yes` or `No`.
7. Required fields are checked.
8. The processed dataframe is serialized to `faculty_data.pkl`.
9. The Streamlit app reloads or the one-hour cache expires.

### Application query flow

1. Streamlit calls `load_faculty_data()`.
2. If `faculty_data.pkl` is missing, the app displays an error and stops.
3. The function loads the dataframe and extracts individual specialization values.
4. The user interacts with the multiselect, checkbox, and name field.
5. The app starts with a copy of the complete dataframe.
6. The teaching filter is applied first.
7. The specialization filter is applied next.
8. The name filter is applied last.
9. Matching rows are sorted through department grouping.
10. The display table is built and rendered as HTML.

## Data model

The prepared dataframe has the following application-facing fields:

| Field | Source type | Purpose |
|---|---|---|
| `faculty_name` | String | Display name used for text search and result rows |
| `department` | String | Used to group and organize results |
| `specialization` | String | Comma-separated expertise values used for discovery and filtering |
| `currently_teaching` | String | Normalized to `Yes` or `No` |
| `experience` | String/number | Displayed in the results table when present |
| `research_papers` | String/number | Displayed in the results table when present |
| `google_scholar_link` | String | Converted to a clickable profile link |

The current UI also expects `faculty_name`, `department`, `specialization`, and `currently_teaching` in its filtering path. The preparation script treats `faculty_name`, `department`, `specialization`, and `currently_teaching` as required columns. `experience`, `research_papers`, and `google_scholar_link` are optional at the column-mapping level and are included only when present.

### Source-to-standard column mapping

The preparation script cleans raw source headers by:

1. Removing characters other than letters, digits, underscores, and spaces.
2. Replacing spaces with underscores.
3. Converting the result to lowercase.

It then recognizes common source-header phrases and maps them to the stable names above:

| Stable field | Header text it recognizes |
|---|---|
| `faculty_name` | `enter_your_name_capital_letters_are_preferred` |
| `department` | `select_your_department` |
| `specialization` | `kindly_select_the_your_respective_specialization` |
| `experience` | `experience_in_the_relevant_specialization` |
| `research_papers` | `number_of_research_paper_published_so_far` |
| `google_scholar_link` | `kindly_give_me_the_links_of_the_google_scholar` |
| `currently_teaching` | `are_you_currently_teaching_subject_related_to_your_specialization` |

Headers that do not match a recognized phrase remain available under their cleaned, lowercase, underscore-separated name.

## Repository structure

```text
.
|-- SME_Tech_Guru.py       # Streamlit application and browser UI
|-- 01_prepare_data.py      # Google Sheets data refresh pipeline
|-- faculty_data.pkl        # Cached prepared faculty dataframe
|-- requirements.txt        # Runtime Python dependencies
|-- README.md               # Project documentation
`-- .streamlit/
    `-- config.toml         # Streamlit visual theme and server settings
```

## Installation

### Requirements

- Python 3.10 or newer is recommended
- Internet access for the data refresh script
- A supported browser
- Public read access to the configured Google Sheet

### Install dependencies

From the repository directory:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The core packages are:

- `streamlit`
- `pandas`

Python's standard library supplies the remaining imports:

- `pickle`
- `os`
- `re`

## Running the application

From the repository directory:

```powershell
python -m streamlit run SME_Tech_Guru.py
```

Then open the local URL printed by Streamlit, normally:

```text
http://localhost:8501
```

The app is also reachable through a network URL if Streamlit displays one.

## Refreshing faculty data

Run the preparation script whenever the Google Sheet changes:

```powershell
python 01_prepare_data.py
```

The script:

- Downloads the sheet as CSV
- Processes it
- Replaces `faculty_data.pkl`
- Prints the final column names and the first five rows

The sheet must be shared as **Anyone with the link can view** unless the environment supplies an alternative authenticated export mechanism.

Restarting Streamlit or clearing the Streamlit cache may be necessary if an existing process holds a cached dataframe longer than desired.

## Google Sheets configuration

The sheet URL is configured as `GOOGLE_SHEET_URL` in `01_prepare_data.py`.

To use another sheet:

1. Open `01_prepare_data.py`.
2. Replace `GOOGLE_SHEET_URL` with the full Google Sheets edit/share URL.
3. Ensure the sheet contains the expected faculty form headers.
4. Share the sheet with public view access.
5. Run the preparation script.

The sheet must expose a first worksheet or CSV export that Pandas can parse successfully. Renaming source headers can break automatic field mapping unless the matching phrase in the script is updated too.

## Filtering behavior

The three filter types are combined using logical AND:

- **Teaching state:** applies only if the checkbox is enabled.
- **Specialization:** any selected specialization may match.
- **Faculty name:** contains the entered text.

For specialization filtering:

- A field containing comma-separated values is searched for a case-insensitive substring match.
- All selected values are tested with an OR relationship.
- The selected specialization values do not need to match from the start of the text.

For name filtering:

- Search text is converted to lowercase.
- Leading and trailing whitespace is removed.
- Faculty names are searched with `case=False`.

## UI and theming

The app uses a wide layout and starts with the sidebar collapsed.

The `.streamlit/config.toml` theme defines:

| Setting | Value |
|---|---|
| Primary color | `#4CAF50` |
| Background | `#FFFFFF` |
| Secondary background | `#F0F2F6` |
| Text | `#262730` |
| Font | Sans-serif |

Additional CSS in `SME_Tech_Guru.py` controls:

- Main title and tagline
- Section headers
- Widget labels
- Container spacing
- Table typography
- Row zebra striping
- Hover highlighting
- Google Scholar link styling

The Streamlit footer and menu are hidden for a cleaner application-style presentation.

## Error handling

### Missing faculty data

If `faculty_data.pkl` is absent:

- The app displays an error telling the maintainer to run `01_prepare_data.py`.
- It returns an empty dataframe and an empty specialization list.
- The main application displays a critical error and stops.

### Corrupt or unreadable faculty data

If the pickle cannot be opened or loaded:

- The app catches the exception.
- It displays an error suggesting that the file be regenerated.
- It returns no usable faculty records.

### Missing required sheet columns

During preparation, the script validates:

- `faculty_name`
- `department`
- `specialization`
- `currently_teaching`

If any is missing after header normalization, preparation stops and prints a message describing the issue.

### Other refresh failures

Preparation handles empty CSV data separately and also provides general guidance for:

- Internet connectivity problems
- Incorrect sheet URLs
- Sheets that are not publicly accessible
- Unexpected source-header names

## Deployment

The application can be deployed wherever Streamlit is supported. Before deployment:

1. Add the repository to the hosting environment.
2. Install `requirements.txt`.
3. Include or generate `faculty_data.pkl`.
4. Set the Streamlit entry point to `SME_Tech_Guru.py`.
5. Configure public/private access as required.
6. Provide network access to Google Sheets if data should refresh at runtime or during scheduled builds.

The app does not currently run `01_prepare_data.py` automatically. It only reads `faculty_data.pkl`, so a deployed instance must receive an up-to-date pickle file or have a separate refresh job generate it.

## Security and privacy

This project is suitable for a public faculty directory, but maintainers should consider:

- Google Scholar and contact links may expose public professional information.
- The source sheet may contain names or personal details and should not be publicly shared unless intended.
- The current `faculty_data.pkl` is an executable Python serialization format. It should only be loaded from a trusted source.
- The app inserts dataframe values into HTML using `unsafe_allow_html=True`, so upstream text should be treated as potentially unsafe and ideally sanitized before display.
- URLs are displayed as profile links but are not validated by an allowlist.
- The application has no authentication, authorization, or role-based access control.
- It has no audit log for searches or data refreshes.

For a production deployment, consider maintaining a CSV or database as the source of truth, validating and escaping all fields, restricting sheet access, and introducing explicit URL validation.

## Limitations

- There is no database or API backend.
- There is no automatic refresh schedule.
- The application depends on Google Sheet header phrases.
- The cache may retain stale data for up to one hour.
- Data must be refreshed manually unless a separate process is scheduled.
- The prepared pickle is not human-readable.
- Loading untrusted pickle files is unsafe.
- There is no pagination or server-side search.
- Department and specialization values are not normalized beyond trimming at the specialization extraction step.
- Names are searched only by substring matching.
- No authentication or audit trail is implemented.
- The app does not expose a data-management/admin interface.
- Google Scholar links are not checked for reachability.

## Troubleshooting

### Streamlit will not start

Verify that dependencies are installed and that Streamlit is running with the intended Python interpreter:

```powershell
python -m pip show streamlit pandas
python -m streamlit --version
python -m streamlit run SME_Tech_Guru.py
```

### The sheet refresh fails

Check that:

- The sheet URL contains `/d/<spreadsheet-id>/`.
- The sheet is publicly viewable.
- The sheet export contains a parseable CSV.
- Source headers have not changed in ways that prevent required-column mapping.
- The current environment has internet access.

### Required column messages appear

Compare the sheet's raw headers with the matching phrases in `01_prepare_data.py`. Keep the current header wording or update the mapping logic when a form header changes.

### Faculty data is missing in the app

Run:

```powershell
python 01_prepare_data.py
```

Then verify that `faculty_data.pkl` exists in the repository root and that Streamlit is started from the repository root. Relative file paths mean the app should be launched from the directory containing the scripts and pickle file.

### Data changes do not appear immediately

Streamlit caches the app data for one hour. Restart the app or clear Streamlit's cache, then refresh the browser.

### HTML or table content looks incorrect

Confirm that:

- Department values are not missing or inconsistently spelled.
- Specialization values are strings or can safely be converted to strings.
- The dataframe contains no malformed data types.
- No duplicate or outdated Streamlit styling is overriding the custom CSS.

## Maintainer guide

### Adding a display field

To show a new field:

1. Confirm that it exists after Google Sheet header mapping.
2. Add it to the `display_column_map` in `SME_Tech_Guru.py`.
3. Add a user-friendly label.
4. Refresh `faculty_data.pkl`.
5. Verify that missing values do not break rendering.

### Adding a new filter

1. Add a Streamlit widget with a stable `key`.
2. Apply the filter to a copy of `faculty_df`.
3. Ensure the filter works with specialization and name filtering.
4. Test with missing and unexpected values.
5. Update the filter documentation in this README.

### Changing the source sheet

Update `GOOGLE_SHEET_URL`, run the preparation script, inspect its processed-column output, and verify that all required fields remain present.

### Updating the design

The reusable theme is in `.streamlit/config.toml`. Finer styling for titles, tables, widgets, and containers is in the inline CSS block near the top of `SME_Tech_Guru.py`.
