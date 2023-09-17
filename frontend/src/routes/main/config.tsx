import { RouteObject } from "react-router-dom";
import React from "react";

// Import Components Here (Lazily)
const Main = React.lazy(() => import('./main'))
const Home = React.lazy(() => import('../../pages/index'))
const Faq = React.lazy(() => import('../../pages/faq'))

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
    }, {
      path : "faq",
      element : <Faq />
    }]
  }
]

export default routes
