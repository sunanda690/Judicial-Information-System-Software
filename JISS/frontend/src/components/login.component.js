import React, { Component } from "react";
import axios from 'axios';
import '../../node_modules/bootstrap/dist/css/bootstrap.min.css';
import './login.css';

import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    Redirect
} from "react-router-dom";

class Welcome extends Component {
    render() {
        return (
            <div ><h1>Welcome to JISS</h1></div>
        );
    }
}
export default class Login extends Component {
    constructor(props) {
        super(props);
        this.state = { username: '', password: '', username_error: false, password_error: false };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({ [event.target.name]: event.target.value });
        if (event.target.value == "") {
            this.setState({ [event.target.name + '_error']: true });
        }
    }
    handleSubmit(event) {
        //console.log('Submitting'); //For Debug
        var errors = {
            username_error: false,
            password_error: true
        };
        var flag = false;

        //Form Validation
        if (this.state.username == "") {
            this.setState({ username_error: true });
            errors.username_error = true;
            flag = true;
        }
        else {
            this.setState({ username_error: false });
            errors.username_error = false;
        }

        if (this.state.password == "") {
            this.setState({ password_error: true });
            errors.password_error = true;
            flag = true;
        }
        else {
            this.setState({ password_error: false });
            errors.password_error = false;
        }

        if (!flag) {
            //alert('A username was submitted: ' + this.state.username);
            const requestOptions = {
                'username': this.state.username, 'password': this.state.password
            };
            console.log("LoggingIn ")
            axios.post('/api/login', requestOptions)
                .then(res => {
                    console.log(res.data);
                    if(res.data.login_status=="0")
                    {
                        alert("Invalid Username or Password");
                    }
                    this.props.handlelogin(res.data);

                });
            event.preventDefault();
        }




    }
    render() {

        if (this.state.login) {
            return (<Redirect to="/home" />)
        }
        else {
            return (
                <div className="Login">
                    <header className="Login-header">
                        <Welcome />
                        <form onSubmit={this.handleSubmit}>
                            <h3>Please Sign In</h3>

                            <div className="form-group">
                                <label>Username</label>
                                <input type="text" name="username" onChange={this.handleChange} className="form-control" placeholder="Enter Username" />
                                {this.state.username_error ? <div style={{ color: "red" }}>Username cannot be Empty</div> : ""}
                            </div>
                            <br />
                            <div className="form-group">
                                <label>Password</label>
                                <input type="password" name="password" onChange={this.handleChange} className="form-control" placeholder="Enter password" />
                                {this.state.password_error ? <div style={{ color: "red" }}>Password cannot be Empty</div> : ""}
                            </div>
                            {/*
                    <div className="form-group">
                        <div className="custom-control custom-checkbox">
                            <input type="checkbox" className="custom-control-input" id="customCheck1" />
                            <label className="custom-control-label" htmlFor="customCheck1">Remember me</label>
                        </div>
                    </div>*/}

                            <button type="submit" className="btn btn-primary btn-block">Submit</button>
                            {/*<p className="forgot-password text-right">
                        Forgot <a href="#">password?</a>
                </p>*/}
                        </form>
                    </header>
                </div>
            );
        }

    }
}