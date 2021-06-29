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
export default class QueryResolved extends Component {
    constructor(props) {
        
        super(props);
        this.state = {

            beg_date: null,
            end_date: null,
            case_list: null,
            data_recv: false,            

            beg_date_error: false,
            end_date_error: false

        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }
    handleSubmit(e) {
        e.preventDefault();
        var flag = false;
        var errors = {
            beg_date_error: false,
            end_date_error: false
        }
        //Validate Form input


        if (this.state.beg_date == null) {
            this.setState({ beg_date_error: true });
            errors.beg_date_error = true;
            flag = true;
        }
        else {
            this.setState({ beg_date_error: false });
            errors.beg_date_error = false;
        }

        if (this.state.end_date == null) {
            this.setState({ end_date_error: true });
            errors.end_date_error = true;
            flag = true;
        }
        else {
            this.setState({ end_date_error: false });
            errors.end_date_error = false;
        }

        //Data Consistency Check

        if(this.state.beg_date>this.state.end_date)
        {
            alert('Start Date Cannot be After End date');
            flag = true;
        }

        if (!flag) {
            const requestOptions = {
                'beg_date': {
                    'day': this.state.beg_date.getDate().toString(),
                    'month': (this.state.beg_date.getMonth() + 1).toString(),
                    'year': this.state.beg_date.getFullYear().toString()
                },
                'end_date': {
                    'day': this.state.end_date.getDate().toString(),
                    'month': (this.state.end_date.getMonth() + 1).toString(),
                    'year': this.state.end_date.getFullYear().toString()
                }
            };
            axios.post('/api/queryResolved', requestOptions)
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
                                        starting_date: new Date(parseInt(item.starting_date.year), parseInt(item.starting_date.month) - 1, parseInt(item.starting_date.day)),
                                        name_pres_judge: item.name_pres_judge,
                                        latest_date: new Date(parseInt(item.latest_date.year), parseInt(item.latest_date.month) - 1, parseInt(item.latest_date.day)),
                                        case_summary: item.case_summary
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
                            <h3>Query Resolved Cases</h3>

                            <div className="form-group">
                                Starting Date: <DatePicker dateFormat="dd-MM-y" selected={this.state.beg_date} onChange={date => {
                                    this.setState({ beg_date: date }); this.setState({ data_recv: false });
                                    (!date) ? this.setState({ beg_date_error: true }) : this.setState({ beg_date_error: false });
                                }} />
                                {this.state.beg_date_error ? <div style={{ color: "red" }}>Starting Date cannot be Empty</div> : ""}
                            </div>

                            <div className="form-group">
                                Ending Date: <DatePicker dateFormat="dd-MM-y" selected={this.state.end_date} onChange={date => {
                                    this.setState({ end_date: date }); this.setState({ data_recv: false });
                                    (!date) ? this.setState({ end_date_error: true }) : this.setState({ end_date_error: false });
                                }} />
                                {this.state.end_date_error ? <div style={{ color: "red" }}>Ending Date cannot be Empty</div> : ""}
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
                                        <AgGridColumn field="starting_date" sortable="true"></AgGridColumn>
                                        <AgGridColumn field="cin"></AgGridColumn>                                        
                                        <AgGridColumn field="name_pres_judge"></AgGridColumn>
                                        <AgGridColumn field="latest_date"></AgGridColumn>
                                        <AgGridColumn field="case_summary"></AgGridColumn>                                        
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