import { RouteObject } from "react-router-dom";
import React from "react";
import Alumni from "../../pages/alumni";
import Multimedia from "../../pages/multimedia/multimedia";
import { NavTabRoute } from "../../core/types";
import { mainLoader, redirectLoader } from "./main";

// Import Components Here (Lazily)
const Main = React.lazy(() => import("./main"));
const Home = React.lazy(() => import("../../pages/index"));
const Faq = React.lazy(() => import("../../pages/faq"));
const QueryFallback = React.lazy(
  () => import("../../components/QueryFallback")
);
const AboutUs = React.lazy(() => import("../../pages/about-us"));
const Blog = React.lazy(() => import("../../pages/blog"));
const SlugBlog = React.lazy(() => import("../../pages/blog/slug"));
const Links = React.lazy(() => import("../../pages/resources/links"));
const Shorten = React.lazy(() => import("../../pages/shorten"));

/**
 * @brief refer to https://reactrouter.com/en/main/hooks/use-routes
 */
export const tabRoutes: NavTabRoute[] = [
  {
    path: "about-us",
    element: <AboutUs />,
    tabName: "About Us",
  },
  // {
  //   path: "events",
  //   element: <Events />,
  //   tabName: "Events",
  // },
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
    path: "multimedia",
    element: <Multimedia />,
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
      ...tabRoutes,
      // {
      //   path: "links",
      //   element: <Links />,
      // },
      // {
      //   path: "shorten",
      //   children: [
      //     {
      //       path: ":slug",
      //       element: <Shorten />,
      //     },
      //   ],
      // },
      {
        path: "*",
        loader: redirectLoader,
      }
    ],
  },
];

export default routes;
