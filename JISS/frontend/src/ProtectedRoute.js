import { Component } from "react";
import { Route, Redirect } from "react-router-dom";
import Auth from './Auth';
export default function ProtectedRoute({children,...rest}) {
    return (
        <Route            
            render={(props) =>
                Auth() ? (                    
                    children
                ) : (
                    <Redirect
                        to={{
                            pathname: "/login",                            
                        }}
                    />
                )
            }
        />
    )

}
