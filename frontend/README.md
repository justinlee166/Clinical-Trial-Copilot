# Clinical Trial Copilot - Frontend

A modern React frontend for the Clinical Trial Copilot, providing an intuitive interface for uploading PDFs and viewing AI-powered analysis results.

## Features

- 📄 **PDF Upload**: Drag-and-drop or click-to-upload interface
- 🔄 **Real-time Progress**: Live progress tracking during analysis
- 📊 **Results Display**: Structured clinical trial data presentation
- 🧠 **AI Insights**: Claude AI analysis and recommendations
- 📈 **Visualizations**: Interactive chart viewer with download options
- 📁 **Export Options**: Download results in multiple formats (JSON, CSV, PDF)
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile

## Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **Lucide React** - Beautiful icons

## Quick Start

### Prerequisites

- Node.js 16+ and npm
- Backend server running on `http://localhost:8000`

### Installation

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Navigate to `http://localhost:3000`

### Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── FileUpload.jsx   # PDF upload with drag-and-drop
│   │   ├── ProgressBar.jsx  # Loading progress indicator
│   │   ├── ResultsCard.jsx  # Clinical data display
│   │   ├── InsightsCard.jsx # AI analysis display
│   │   ├── ChartViewer.jsx  # Visualization viewer
│   │   └── ExportButtons.jsx # Download options
│   ├── pages/               # Main application pages
│   │   ├── UploadPage.jsx   # PDF upload interface
│   │   └── ResultsPage.jsx  # Analysis results display
│   ├── services/            # API integration
│   │   └── api.js          # Backend API calls
│   ├── App.jsx             # Main application component
│   ├── main.jsx            # Application entry point
│   └── index.css           # Global styles
├── public/                 # Static assets
├── package.json           # Dependencies and scripts
├── vite.config.js         # Vite configuration
├── tailwind.config.js     # Tailwind CSS configuration
└── README.md             # This file
```

## Usage

### Upload and Analyze

1. **Upload PDF**: Drag and drop or click to select a clinical trial PDF
2. **Start Analysis**: Click "Start Analysis" to begin processing
3. **View Progress**: Watch real-time progress updates
4. **Review Results**: Explore structured data, AI insights, and visualizations
5. **Export Data**: Download results in your preferred format

### API Integration

The frontend communicates with the backend through these endpoints:

- `POST /analyze` - Upload and analyze PDF
- `GET /status/{id}` - Check analysis status
- `GET /results/{id}` - Get analysis results
- `GET /download/{id}/{type}` - Download files
- `GET /health` - Health check

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Customization

- **Styling**: Modify `tailwind.config.js` for theme customization
- **Components**: Add new components in `src/components/`
- **Pages**: Create new pages in `src/pages/`
- **API**: Extend `src/services/api.js` for new endpoints

## Deployment

### Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

### Environment Configuration

For production, update the `VITE_API_BASE_URL` environment variable to point to your production backend URL.

## Troubleshooting

### Common Issues

1. **Backend Connection Error**
   - Ensure backend is running on `http://localhost:8000`
   - Check `VITE_API_BASE_URL` in `.env` file

2. **File Upload Issues**
   - Verify file is a valid PDF
   - Check file size limits
   - Ensure backend API is accessible

3. **Build Errors**
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check Node.js version compatibility

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the Clinical Trial Copilot system.
