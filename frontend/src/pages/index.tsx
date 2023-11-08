import React from "react";
import Navbar from "../core/navbar"; // Import the Navbar component
import Footer from "../core/footer"
import fakeNavbarData from "../core/fakeDataForNavbar"; // Import the fake data
import fakeFooterData from "../core/fakeDataForFooter";

const Home = () => {
  return (
    <Navbar config = {fakeNavbarData} />
  )
}

export default Home
