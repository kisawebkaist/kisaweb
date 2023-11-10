import React from "react";
import Navbar from "../core/navbar"; // Import the Navbar component
import Footer from "../core/footer"
import fakeNavbarData from "../core/fakeDataForNavbar"; // Import the fake data
import fakeFooterData from "../core/fakeDataForFooter";

import NavEntryT from "../core/navbar-type";
import { useState, useEffect } from "react";
import { FooterT } from "../API/misc";

// Zwe: Just testing, feel free to delete this
const api_endpoint = process.env.REACT_APP_API_ENDPOINT;

function Home() {
  const [navbar, setNavbar] = useState<NavEntryT[]>([]);
  const [footer, setFooter] = useState<FooterT>();

  useEffect(()=>{
    fetch(api_endpoint+"misc/navbar")
    .then((res) => res.json())
    .then((json) => setNavbar(json))

    fetch(api_endpoint+"misc/footer")
    .then((res) => res.json())
    .then((json) => setFooter(json))

  }, []);
  return (
    <Navbar config={navbar} />
  );
}

// const Home = () => {
//   return (
//     <Navbar config = {fakeNavbarData} />
//   )
// }

export default Home
