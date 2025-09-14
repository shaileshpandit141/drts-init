import React from 'react';
import ReactDOM from 'react-dom/client';
import "styles/reset.css";
import "styles/theme.css";
import "styles/variables.css";
import "styles/typography.css";
import "styles/root.css";
import { Provider } from "react-redux";
import { store } from "app/store";
import RootRoutes from "routes";
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <RootRoutes />
    </Provider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
