## Printing & PDF

### PDF Generation
- Use ReportLab to render a consistent weekly layout
- Template fields: title, week range, per-day sections with categories
- Fonts: system sans-serif; support simple theming later
- Store PDFs under `var/prints/YYYY/Week-YYYY-MM-DD.pdf`

### Print Pipeline
- Windows: use `pywin32` (`win32print`) to send PDF to default printer
- macOS/Linux: provide PDF download; optional CUPS integration in future
- Print preview page embeds the generated PDF

### Commands
- Management command `weekly_print`:
  - Generate plan for the upcoming week (next Monday)
  - Render PDF and save path to `WeeklyPlan`
  - If on Windows and printing enabled, send to printer

### Error Handling
- If printing fails, keep PDF and surface message with retry button
- Log all errors to `var/logs/app.log`

### Future
- Customizable templates (logo, fonts, margins)
- Multi-page support

### Adapter Design
- `PrinterAdapter` determines behavior via configuration:
  - `PdfOnlyPrinter` (default in dev): generate and store PDF; no print
  - `WindowsPrinter`: use `pywin32` to send job to default printer
  - `SumatraPrinter` (optional fallback): shell to `SumatraPDF -silent -print-to-default <file.pdf>`
- Configuration:
  - `PRINTING_MODE=none|windows|sumatra`
  - In dev (Mac), use `none`; on Windows, prefer `windows` and allow `sumatra` as fallback
- Logging:
  - Record printer selection, target device, job success/failure, and retry guidance
