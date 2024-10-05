import { RouteObject } from "react-router-dom";
import React from "react";
import Alumni from "../pages/alumni";
import { NavTabRoute } from "../core/types";
import { MultimediaHomeWithGuard, MultimediaWithGuard } from "../pages/multimedia/multimedia";

// Import Components Here (Lazily)
const Main = React.lazy(() => import("../core/Main"));
const Faq = React.lazy(() => import("../pages/faq/index"));
const QueryFallback = React.lazy(
  () => import("../components/common/QueryFallback")
);
const AboutUs = React.lazy(() => import("../pages/about-us"));
const Blog = React.lazy(() => import("../pages/blog"));
const SlugBlog = React.lazy(() => import("../pages/blog/slug"));
const Event = React.lazy(() => import("../pages/event"));
const Links = React.lazy(() => import("../pages/important-links"));
const Shorten = React.lazy(() => import("../pages/bitly"));
const Election = React.lazy(() => import("../pages/election"));

/**
 * @brief refer to https://reactrouter.com/en/main/hooks/use-routes
 */
export const tabRoutes: NavTabRoute[] = [
  {
    path: "about-us",
    element: <AboutUs />,
    tabName: "About Us",
  },
  {
    path: "blog",
    children: [
      {
        index: true,
        element: <Blog />,
      },
      {
        path: ":slug",
        element: <SlugBlog />,
      },
    ],
    tabName: "Blog",
  },
  {
    path: "event",
    element: <Event />,
    tabName: "Event"
  },
  {
    path: "faq",
    element: <Faq />,
    tabName: "FAQ",
  },
  {
    path : "important-links",
    element : <Links />,
    tabName : "Important Links"
  },
  {
    path: "multimedia",
    children: [
      {
        path: "",
        element: <MultimediaHomeWithGuard />
      },
      {
        path: ":slug",
        element: <MultimediaWithGuard />
      }
    ],
    tabName: "Multimedia",
  },
  {
    path: "alumni",
    element: <Alumni />,
    tabName: "Alumni"
  },
  {
    path: "election",
    element: <Election />,
    tabName: "election",
  },
]

export const routes: RouteObject[] = [
  {
    path: "/",
    element: <Main />,
    children: [
      {
        index: true,
        element: tabRoutes[0].element,
      },
      {
        path : 'bitly/:slug',
        element : <Shorten />
      },
      ...tabRoutes,
      {
        path: "*",
        element : <QueryFallback />
      }
    ],
  },
];

export default routes;
