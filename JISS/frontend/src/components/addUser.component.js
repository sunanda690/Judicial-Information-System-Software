import React, { Component } from "react";
import GridLayout from 'react-grid-layout';
import axios from 'axios';
import Dropdown from "react-dropdown";
import 'bootstrap/dist/css/bootstrap.min.css';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import './registrar.css';
import { BrowserRouter as Router } from "react-router-dom";
import LogoutButton from "./logoutbutton"
import './form.css';
export default class AddUser extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: "",
            usr_name: "",
            password: "",
            usr_type: "None",
            usr_addr: "",
            usr_name_error: false,
            username_error: false,
            password_error: false,
            usr_type_error: false,
            usr_addr_error: false
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }
    handleSubmit(e) {
        e.preventDefault();
        var errors = {
            usr_name_error: false,
            username_error: false,
            password_error: false,
            usr_type_error: false,
            usr_addr_error: false
        }
        //Validate Form input
        if (this.state.usr_name == "") {
            this.setState({ usr_name_error: true });
            errors.usr_name_error = true;
        }
        else {
            this.setState({ usr_name_error: false });
            errors.usr_name_error = false;
        }
        if (this.state.password.length < 3) {
            this.setState({ password_error: true });
            errors.password_error = true;
        }
        else {
            this.setState({ password_error: false });
            errors.password_error = false;
        }
        if (this.state.username == "") {
            this.setState({ username_error: true });
            errors.username_error = true;
        }
        else {
            this.setState({ username_error: false });
            errors.username_error = false;
        }
        if (this.state.usr_type == "None") {
            this.setState({ usr_type_error: true });
            errors.usr_type_error = true;
        }
        else {
            this.setState({ usr_type_error: false });
            errors.usr_type_error = false;
        }

        if (this.state.usr_addr == "") {
            this.setState({ usr_addr_error: true });
            errors.usr_addr_error = true;
        }
        else {
            this.setState({ usr_addr_error: false });
            errors.usr_addr_error = false;
        }

        if (!(errors.usr_name_error || errors.password_error || errors.username_error || errors.usr_addr_error || errors.usr_type_error)) {
            console.log('Data to be Sent : ', this.state);
            const requestOptions = {
                'username': this.state.username, 'password': this.state.password,
                'name': this.state.usr_name, 'usr_type': this.state.usr_type,
                'usr_addr': this.state.usr_addr
            };
            axios.post('/api/addUser', requestOptions)
                .then(res => {
                    console.log(res.data);
                    if (res.data.add_status == "0") {
                        alert(res.data.err_msg);
                    }
                    else {
                        alert('User Added Successfully');
                        // this.props.goback();//Optional
                    }
                })
                .catch(err => {
                    alert('Error in Server ' + err.response.status);
                    console.log(err.response);
                });
        }

    }
    handleChange(e) {
        this.setState({ [e.target.name]: e.target.value }, () => {
            if (e.target.name == "usr_type") {
                if (e.target.value == "None") {
                    this.setState({ usr_type_error: true });
                }
                else {
                    this.setState({ usr_type_error: false });
                }
            }
            else if (e.target.name == "password") {
                if (e.target.value.length < 3) {
                    this.setState({ password_error: true });
                }
                else {
                    this.setState({ password_error: false });
                }
            }
            else {
                if (e.target.value == "") {
                    this.setState({ [e.target.name + "_error"]: true });
                }
                else {
                    this.setState({ [e.target.name + "_error"]: false });
                }
            }
        });

    }
    render() {
        return (
            <Router>
                <div className="Registrar">
                    <div className="Registrar-header">
                        <button
                            onClick={this.props.goback}
                            style={{ marginLeft: "auto" }}
                            className="btn btn-primary "
                        >
                            Go Back
                    </button>
                        <form onSubmit={this.handleSubmit}>
                            <h3>Add User</h3>

                            <div className="form-group">
                                <label>Name</label>
                                <input type="text" name="usr_name" onChange={this.handleChange} className="form-control" placeholder="EnterName" />
                                {this.state.usr_name_error ? <div style={{ color: "red" }}>Name cannot be Empty</div> : ""}
                            </div>
                            <div className="form-group">
                                <label>User Type:</label>
                                <label>
                                    <select className="form-control" defaultValue="None" name="usr_type" onChange={this.handleChange}>
                                        <option value="None">Select User Type</option>
                                        <option value="Lawyer">Lawyer</option>
                                        <option value="Judge">Judge</option>
                                    </select>
                                </label>
                                {this.state.usr_type_error ? <div style={{ color: "red" }}>User Type must be Selected</div> : ""}
                            </div>
                            <div className="form-group">
                                <label>User Address</label>
                                <input type="text" name="usr_addr" onChange={this.handleChange} className="form-control" placeholder="EnterUserAddr" />
                                {this.state.usr_addr_error ? <div style={{ color: "red" }}>Address cannot be Empty</div> : ""}
                            </div>
                            <div className="form-group">
                                <label>Username</label>
                                <input type="text" name="username" onChange={this.handleChange} className="form-control" placeholder="EnterUsername" />
                                {this.state.username_error ? <div style={{ color: "red" }}>Username cannot be Empty</div> : ""}
                            </div>
                            <br />
                            <div className="form-group">
                                <label>Password</label>
                                <input type="password" name="password" onChange={this.handleChange} className="form-control" placeholder="EnterPassword" />
                                {this.state.password_error ? <div style={{ color: "red" }}>At least 3 characters</div> : ""}
                            </div>
                            <div className="form-group">
                                <button type="submit" className="btn btn-primary btn-block">Submit</button>
                            </div>
                        </form>
                    </div>
                </div>
            </Router>
        );
    }
}