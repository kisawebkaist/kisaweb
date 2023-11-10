import NavEntryT from "./navbar-type"; // Import the NavEntryT type

// Fake data for the navigation bar
const fakeNavbarData: NavEntryT[] = [
  {
    type: "link",
    data: {
      href: "/home",
      text: "Home",
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
      href: "/about",
      text: "About",
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
      display: "Dropdown",
      entries: [
        {
          type: "link",
          data: {
            href: "/item1",
            text: "Item 1",
          },
        },
        {
          type: "link",
          data: {
            href: "/item2",
            text: "Item 2",
          },
        },
      ],
    },
  },
  {
    type: "dropdown",
    data: {
      display: "Dropdown2",
      entries: [
        {
          type: "link",
          data: {
            href: "/item1",
            text: "Item 1",
          },
        },
        {
          type: "link",
          data: {
            href: "/item2",
            text: "Item 2",
          },
        },
      ],
    },
  },
];

export default fakeNavbarData;
