import React, { createContext, useEffect, useState } from "react";


export const UserContext = createContext();

export const UserProvider = (props) => {
    //token
    const [token , setToken] = useState(localStorage.getItem("leadsToken"));

    useEffect(() => {
        //fxn to fetch the user i.e the endpoint /api/users/me
        const fetchUser = async () => {
            const requestOptions = {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + token,
                },
            };
            //make the request
            const response = await fetch("/api/users/me", requestOptions);

            if(!response.ok) {
                setToken(null);
            } 
            localStorage.setItem("leadsToken", token);
        };
        fetchUser();
    }, [token]);
    return (
        <UserContext.Provider value = {[token, setToken]}>
             {props.children}
        </UserContext.Provider>
       
    );
}