import { RouteObject } from "react-router-dom";
import React from "react";

// Import Components Here (Lazily)
const Main = React.lazy(() => import('./main'))
const Home = React.lazy(() => import('../../pages/home'))

/**
 * @brief refer to https://reactrouter.com/en/main/hooks/use-routes
 */
const routes : RouteObject[] = [
  {
    path : "/",
    element : <Main />,
    children : [{
      index : true,
      element : <Home />
    }]
  }
]

export default routes
