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
import { AgGridColumn, AgGridReact } from 'ag-grid-react';

import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-balham-dark.css';
/**
 * props : goback
 */
export default class QueryUpcoming extends Component {
    constructor(props) {

        super(props);
        this.state = {

            query_date: null,
            case_list: null,
            data_recv: false,

            query_date_error: false

        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }
    handleSubmit(e) {
        e.preventDefault();
        var flag = false;
        var errors = {
            query_date_error: false,
        }
        //Validate Form input


        if (this.state.query_date == null) {
            this.setState({ query_date_error: true });
            errors.query_date_error = true;
            flag = true;
        }
        else {
            this.setState({ query_date_error: false });
            errors.query_date_error = false;
        }

        if (!flag) {
            const requestOptions = {
                'query_date': {
                    'day': this.state.query_date.getDate().toString(),
                    'month': (this.state.query_date.getMonth() + 1).toString(),
                    'year': this.state.query_date.getFullYear().toString()
                }

            };
            axios.post('/api/queryUpcomingByDate', requestOptions)
                .then(res => {
                    console.log(res.data);
                    if (res.data.confirm == "0") {
                        alert(res.data.message);
                        this.setState({ data_recv: false });
                    }
                    else {
                        this.setState({
                            data_recv: true,
                            case_list: res.data.case_list.map((item) => {
                                return (
                                    {
                                        cin: item.cin,
                                        slot: item.slot,
                                        name_pres_judge: item.name_pres_judge,
                                        crime_type :item.crime_type
                                    }
                                );
                            })
                        })
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
        this.setState({ data_recv: false });
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
                            <h3>Query Upcoming Cases on a Date</h3>

                            <div className="form-group">
                                Enter Date: <DatePicker dateFormat="dd-MM-y" selected={this.state.query_date} onChange={date => {
                                    this.setState({ query_date: date }); this.setState({ data_recv: false });
                                    (!date) ? this.setState({ query_date_error: true }) : this.setState({ query_date_error: false });
                                }} />
                                {this.state.query_date_error ? <div style={{ color: "red" }}>Query Date cannot be Empty</div> : ""}
                            </div>

                            <div className="form-group">
                                <button type="submit" className="btn btn-primary btn-block">Submit</button>
                            </div>
                        </form>
                        {
                            this.state.data_recv ?
                                <div className="ag-theme-balham-dark" style={{ height: 400, width: 1000 }}>

                                    <AgGridReact
                                        rowData={this.state.case_list}>
                                        <AgGridColumn field="slot" sortable="true"></AgGridColumn>
                                        <AgGridColumn field="cin"></AgGridColumn>
                                        <AgGridColumn field="name_pres_judge"></AgGridColumn>
                                        <AgGridColumn field="crime_type"></AgGridColumn>
                                    </AgGridReact>
                                </div>
                                : null
                        }
                    </div>
                </div>
            </Router>
        );
    }
}