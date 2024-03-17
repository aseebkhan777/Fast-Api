import React, { useContext, useEffect, useState } from "react";

import Register from "./components/Register";

import Header from "./components/Header";
import { UserContext } from "./context/UserContext";
import Table from "./components/Table";
import Login from "./components/Login";


const App = ()=> {
  // Message from root endpoint
  const [message, setMessage ] = useState("");

  // import token from usercontext
  const [token] = useContext(UserContext);

  //fxn that will make request to the api
  const getWelcomeMessage = async () => {
    // Request options
    const requestOptions = {
      method : "GET",
      headers : {
        "Content-Type": "application/json",
      },
    };
    //make the request 
    const response = await fetch("/api", requestOptions);
    const data = await response.json();
    if(!response.ok) {
      console.log("Something went wrong!");
    } else {
      setMessage(data.message);
    }

  };
  useEffect(() => {
    getWelcomeMessage();
  },[]);


  return (
   <>
   <Header title={ message }/>
   <div className="columns">
    <div className="column"></div>
    <div className="column m-5 is-two-thirds">
      {
        !token ? (
          <div className="columns">
            <Register /> <Login />
          </div>
        ) : (
          <Table />
        )
      }
    </div>
    <div className="column"></div>
   </div>
   
   </>

  )
};

export default App;
