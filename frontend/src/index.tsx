import { createRoot } from 'react-dom/client';
import App from './App';

// Global styles for material UI typography
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

const domNode = document.getElementById('root');
if (domNode){
  const root = createRoot(domNode);
  root.render(<App />)
}
