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
/**
 * props : goback
 */
export default class CloseCase extends Component {
    constructor(props) {
        super(props);
        this.state = {
            cin: "",
            

            cin_error: false
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }
    handleSubmit(e) {
        e.preventDefault();
        var flag = false;
        var errors = {
            cin_error: false
        }
        //Validate Form input


        if (this.state.cin == "") {
            this.setState({ cin_error: true });
            errors.cin_error = true;
            flag = true;
        }
        else {
            this.setState({ cin_error: false });
            errors.cin_error = false;
        }
        var numbers = /^[0-9]+$/;
        console.log('During Submit',this.state.cin.match(numbers));
        if(!this.state.cin.match(numbers))
        {
            alert('CIN must be Integer')
            flag = true;
        }
        


        if (!flag) {

            const req = {
                'cin': this.state.cin,
                'case_summary': this.state.case_summary
            }
            axios.post('/api/closeCase', req)
                .then(res => {
                    console.log('Close Case Response', res.data);
                    if (res.data.confirm == "0") {
                        alert(res.data.message);
                    }
                    else {
                        alert('Case ' + this.state.cin + ' was closed successfully ');
                        this.props.goback();
                    }
                })
                .catch(err => {
                    err.response ? alert('Error in Server ' + err.response.status) : console.log(err);
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
        this.setState({ case_status: "" });
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
                            <h3>Query Status of Case</h3>
                            <div className="form-group">
                                <label>Enter CIN: </label>
                                <input type="text" name="cin" onChange={this.handleChange} className="form-control" placeholder="Enter CIN" />
                                {this.state.cin_error ? <div style={{ color: "red" }}>CIN cannot be Empty</div> : ""}
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