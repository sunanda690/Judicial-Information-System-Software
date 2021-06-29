import React, { Component } from "react";
import GridLayout from 'react-grid-layout';

import Dropdown from "react-dropdown";
import 'bootstrap/dist/css/bootstrap.min.css';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import './registrar.css';
import { BrowserRouter as Router } from "react-router-dom";
import { AgGridColumn, AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-balham-dark.css';
import LogoutButton from "./logoutbutton"
import axios from "axios";

function DispUserList(props) {
    
        console.log('Props ',props);
        return (
            <div className="ag-theme-balham-dark" style={{ height: 400, width: 600 }}>
                <AgGridReact
                    rowData={props.usr_list}>
                    <AgGridColumn onCellClicked={props.handleselect} field="username"></AgGridColumn>
                    <AgGridColumn field="name"></AgGridColumn>
                    <AgGridColumn field="usr_type"></AgGridColumn>
                </AgGridReact>
            </div>
        );
    
}

export default class RemoveUser extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            username_error: false,
            comp: null,
            usr_list: null
        };
        this.handleUserselect = this.handleUserselect.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.getuserList = this.getuserList.bind(this);
        
    }
    
    handleUserselect(props) {
        console.log(props);
        if(!props.data.username)
        {
            return;
        }
        alert("Removing " + props.data.username);

        const requestOptions = {
            'username': props.data.username
        };
        axios.post('/api/removeUser', requestOptions)
            .then(res => {
                if (res.data.remove_status == "1") {
                    alert('User ' + props.data.username + ' was removed successfully');
                    if(this.state.comp!=null)
                    {
                        this.getuserList();
                    }
                }
                else {
                    alert(res.data.err_msg);
                }
            })
            .catch(err => {
                err.response ? alert('Error in Server ' + err.response.status) : console.log('Error', err);

            });
    }
    handleSubmit(e) {
        e.preventDefault();
        if (this.state.username == "") {
            this.setState({ username_error: true });
        }
        else {
            const requestOptions = {
                'username': this.state.username
            }
            axios.post('/api/removeUser', requestOptions)
                .then(res => {
                    if (res.data.remove_status == "1") {
                        alert('User ' + this.state.username + ' was removed successfully');
                        //this.props.goback();//Optional                        
                        if(this.state.comp!=null){
                            this.getuserList();
                        }                        
                    }
                    else {
                        alert(res.data.err_msg);
                    }
                })
                .catch(err => {
                    alert('Error in Server ' + err.response.status);
                    console.log(err.response);
                });
        }

    }
    handleChange(e) {
        this.setState({ [e.target.name]: e.target.value });
        if (e.target.value == "") {
            this.setState({ [e.target.name + "_error"]: true });
        }
        else {
            this.setState({ [e.target.name + "_error"]: false });
        }
    }
    getuserList() {
        axios.get('/api/getUserList')
            .then(res => {
                this.setState({ usr_list: res.data.usr_list,comp: <DispUserList usr_list={res.data.usr_list} handleselect={this.handleUserselect} /> },()=>{
                    console.log('Get User',this.state.usr_list);
                })
                
            })
            .catch(err => {
                err.response? alert('Error in Server ' + err.response.status):console.log(err);
                
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
                            <h3>Remove User</h3>
                            <div className="form-group">
                                <label>Username</label>
                                <input type="text" name="username" onChange={this.handleChange} className="form-control" placeholder="EnterUsername" />
                                {this.state.username_error ? <div style={{ color: "red" }}>Username cannot be Empty</div> : ""}
                            </div>
                            <br />
                            <div className="form-group">
                                <button type="submit" className="btn btn-primary btn-block">Submit</button>
                            </div>
                        </form>
                        <button className="btn btn-secondary " onClick={this.getuserList}>Get User List</button>
                        {this.state.comp}
                    </div>
                </div>
            </Router>
        );
    }
}