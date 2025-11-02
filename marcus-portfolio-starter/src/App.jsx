import React, { Suspense } from "react";
import Meta from "./components/Meta"; 

const PortfolioSite = React.lazy(() => import("./PortfolioSite.jsx"));

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  componentDidCatch(error, info) {
    console.error("App ErrorBoundary caught:", error, info);
  }
  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: 24 }}>
          <h1 style={{ fontWeight: 800, fontSize: 24 }}>Something went wrong.</h1>
          <p style={{ whiteSpace: "pre-wrap", marginTop: 12 }}>
            {String(this.state.error)}
          </p>
          <p style={{ marginTop: 12, color: "#475569" }}>
            Open your browser console for details. If this mentions a missing package,
            run <code>npm install</code> again.
          </p>
        </div>
      );
    }
    return this.props.children;
  }
}

export default function App() {
  return (
    <ErrorBoundary>
      {/*Global title & description */}
      <Meta
        title="Marcus Bullock, Senior Data Engineer"
        description="DoD data engineering, ML pipelines, operational analytics, and full-stack data delivery. Azure, Databricks, Power BI, Python, SQL, and LLMs."
      />

      <Suspense
        fallback={
          <div style={{ padding: 24 }}>
            <h1 style={{ fontWeight: 800, fontSize: 24 }}>Loading portfolio…</h1>
            <p style={{ marginTop: 8, color: "#475569" }}>
              If this never loads, check the console (F12 → Console) for errors.
            </p>
          </div>
        }
      >
        <PortfolioSite />
      </Suspense>
    </ErrorBoundary>
  );
}
