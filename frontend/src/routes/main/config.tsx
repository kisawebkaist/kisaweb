import { RouteObject } from "react-router-dom";
import React from "react";
import Alumni from "../../pages/alumni";
import { NavTabRoute } from "../../core/types";
import { mainLoader } from "./main";
import { Multimedia, MultimediaHome } from "../../pages/multimedia/multimedia";

// Import Components Here (Lazily)
const Main = React.lazy(() => import("./main"));
const Home = React.lazy(() => import("../../pages/index"));
const Faq = React.lazy(() => import("../../pages/faq/index"));
const QueryFallback = React.lazy(
  () => import("../../components/QueryFallback")
);
const AboutUs = React.lazy(() => import("../../pages/about-us"));
const Blog = React.lazy(() => import("../../pages/blog"));
const SlugBlog = React.lazy(() => import("../../pages/blog/slug"));
const Links = React.lazy(() => import("../../pages/important-links"));
const Shorten = React.lazy(() => import("../../pages/bitly"));

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
        path: "",
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
        element: <MultimediaHome />
      },
      {
        path: ":slug",
        element: <Multimedia />
      }
    ],
    tabName: "Multimedia",
  },
  {
    path: "alumni",
    element: <Alumni />,
    tabName: "Alumni"
  },
]

export const routes: RouteObject[] = [
  {
    path: "/",
    element: <Main />,
    loader: mainLoader,
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
