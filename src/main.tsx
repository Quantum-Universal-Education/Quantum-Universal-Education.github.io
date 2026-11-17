import {Component,StrictMode,type ErrorInfo,type ReactNode} from "react";
import {createRoot} from "react-dom/client";
import App from "./App";
import "../assets/style.css";
import "./react.css";

class AppErrorBoundary extends Component<{children:ReactNode},{hasError:boolean}> {
  state = {hasError:false};
  static getDerivedStateFromError() { return {hasError:true}; }
  componentDidCatch(error:Error, info:ErrorInfo) {
    console.error("Portfolio rendering failed:",error,info.componentStack);
  }
  render() {
    if (this.state.hasError) return <main className="wrap app-error" role="alert">
      <h1>This page could not be rendered.</h1>
      <p>An unexpected error occurred. Reload the page to try again.</p>
      <button type="button" onClick={()=>window.location.reload()}>Reload page</button>
    </main>;
    return this.props.children;
  }
}

const rootElement = document.getElementById("root");
if (!rootElement) throw new Error("Portfolio mount point #root was not found.");

try {
  createRoot(rootElement).render(<StrictMode><AppErrorBoundary><App/></AppErrorBoundary></StrictMode>);
  document.documentElement.dataset.appMounted = "true";
  window.dispatchEvent(new Event("portfolio:mounted"));
} catch (error) {
  console.error("Portfolio failed to start:", error);
  rootElement.innerHTML = '<main class="wrap app-error" role="alert"><h1>This page could not be loaded.</h1><p>Please reload the page. If the problem continues, contact the site owner.</p><button type="button" onclick="location.reload()">Reload page</button></main>';
}
