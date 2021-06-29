import React, { Component } from "react";
import '../../node_modules/bootstrap/dist/css/bootstrap.min.css';

export default class Navbar extends Component {
    constructor(props)
    {
        super(props);
    }
    render() {

        return (

            <nav class="navbar navbar-expand-lg navbar-light bg-primary">
                <a class="navbar-brand" href="/login">Login</a>
                <a class="navbar-brand" href="/home">Home</a>
                <a class ="navbar-brand" href = "/userType-judge">Dashboard</a>                
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">

                </div>
            </nav>

        );
    }
}