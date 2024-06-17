import NavEntryT from "./types"; // Import the NavEntryT type

// Fake data for the navigation bar
const fakeNavbarData: NavEntryT[] = [
  // {
  //   type: "link",
  //   data: {
  //     href: "/",
  //     text: "Home",
  //     style: {
  //       normal: { color: "blue" },
  //       hover: { color: "red" },
  //       active: { color: "green" },
  //     },
  //   },
  // },
  {
    type: "link",
    data: {
      href: "/about-us",
      text: "About",
      style: {
        normal: { color: "blue" },
        hover: { color: "red" },
        active: { color: "green" },
      },
    },
  },
  {
    type: "link",
    data: {
      href: "/events",
      text: "Events",
      style: {
        normal: { color: "blue" },
        hover: { color: "red" },
        active: { color: "green" },
      },
    },
  },
  {
    type: "link",
    data: {
      href: "/blog",
      text: "Blog",
      style: {
        normal: { color: "blue" },
        hover: { color: "red" },
        active: { color: "green" },
      },
    },
  },
  {
    type: "link",
    data: {
      href: "/faq",
      text: "FAQ",
      style: {
        normal: { color: "blue" },
        hover: { color: "red" },
        active: { color: "green" },
      },
    },
  },
  {
    type: "link",
    data: {
      href: "/multimedia",
      text: "Multimedia",
      style: {
        normal: { color: "blue" },
        hover: { color: "red" },
        active: { color: "green" },
      },
    },
  },
  {
    type: "dropdown",
    data: {
      display: "Welfare",
      entries: [
        {
          type: "link",
          data: {
            href: "/voice",
            text: "KISA Voice",
          },
        },
        {
          type: "link",
          data: {
            href: "/books",
            text: "KISA Books: Buy & Sell",
          },
        },
        {
          type: "link",
          data: {
            href: "/internships",
            text: "Internships",
          },
        },
      ],
    },
  },
  {
    type: "dropdown",
    data: {
      display: "Resources",
      entries: [
        {
          type: "link",
          data: {
            href: "/course-resources",
            text: "Course Resources",
          },
        },
        {
          type: "link",
          data: {
            href: "/links",
            text: "Important Links",
          },
        },
      ],
    },
  },
  {
    type: "link",
    data: {
      href: "/alumni",
      text: "Alumni",
      style: {
        normal: { color: "blue" },
        hover: { color: "red" },
        active: { color: "green" },
      },
    },
  },
  {
    type: "link",
    data: {
      href: "/election",
      text: "Election",
      style: {
        normal: { color: "blue" },
        hover: { color: "red" },
        active: { color: "green" },
      },
    },
  },
];

export default fakeNavbarData;
