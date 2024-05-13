import React, { useEffect, useState } from "react"
import { Outlet } from "react-router-dom"
import Footer, { FooterP } from "../../core/footer"
import Navbar from "../../core/navbar"
import NavEntryT from "../../core/navbar-type"
import "../../components/css/index.css"
import fakeFooterData from "../../core/fakeDataForFooter"
import fakeNavbarData from "../../core/fakeDataForNavbar"

const Main = () => {
  const [navbarConfig, setNavbarConfig] = React.useState<NavEntryT[]>(fakeNavbarData)
  const [footerConfig, setFooterConfig] = React.useState<FooterP>(fakeFooterData)

  // testing code, feel free to remove
  // const [sessionState, setSessionState] = useState<SessionState>(initialSessionState);
  function fetchState() {
    // Here we need csrftoken cookie but in testing environment, backend and frontend are in different origins which is a problem
    const stateEndpoint = process.env.REACT_APP_API_ENDPOINT+'/state';
    fetch(
      stateEndpoint
    ).then((r)=>r.json()).then((response)=>{
      // the response is now of the form {"already_logined": <if the user is authenticated with sso>, "is_verified": <if the user is authenticated with sso and 2nd factor>}
      // the attributes can be changed based on the need from frontend, this endpoint is supposed to be called everytime the website loads as it will set the necessary cookies 
      // and it will return the state information stored in the backend session
    });
  }
  function fetchNavBarAndFooterConfig() {
    const navbarEndpoint = process.env.REACT_APP_API_ENDPOINT+'/misc/navbar';
    const footerEndpoint = process.env.REACT_APP_API_ENDPOINT+'/misc/footer';

    fetch(navbarEndpoint)
    .then(r => r.json())
    .then(setNavbarConfig);

    fetch(footerEndpoint)
    .then(r => r.json())
    .then(setFooterConfig);
  }
  function queryBackend() {
    fetchState();
    fetchNavBarAndFooterConfig();
  }
  useEffect(queryBackend, []);

  // useEffect to query
  return (
    <React.Fragment>
      <header>
        <Navbar config = {navbarConfig} />
      </header>
      <main>
        {/* <div className="mainContent">
          <img src="https://media.tenor.com/CWgfFh7ozHkAAAAC/rick-astly-rick-rolled.gif" width="100%"/>
        </div> */}
        <Outlet />
      </main>
      {footerConfig && <Footer {...footerConfig} />}
    </React.Fragment>
  )
}

export default Main
