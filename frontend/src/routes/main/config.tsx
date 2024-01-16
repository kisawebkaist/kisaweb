import { RouteObject } from "react-router-dom";
import React from "react";

// Import Components Here (Lazily)
const Main = React.lazy(() => import('./main'))
const Home = React.lazy(() => import('../../pages/index'))
const Faq = React.lazy(() => import('../../pages/faq'))
const QueryFallback = React.lazy(() => import ("../../components/QueryFallback"))
const AboutUs = React.lazy(() => import('../../pages/about-us'))
const Blog = React.lazy(() => import('../../pages/blog'))

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
    }, {
      path : 'about-us',
      element : <AboutUs />
    }, 
    {
      path: "blog",
      element: <Blog />
    }, {
      path : "*",
      element : <QueryFallback />
    }]
  }
]

export default routes
