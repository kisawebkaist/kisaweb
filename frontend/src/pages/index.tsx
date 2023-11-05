import React from "react";
import Navbar from "../core/navbar"; // Import the Navbar component
import fakeNavbarData from "../core/fakeDataForNavbar"; // Import the fake data

const Home = () => {
  return (
    <Navbar config = {fakeNavbarData} />
  )
}

export default Home
