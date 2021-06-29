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
 * props: handleselect,goback
 */
export default class ViewPendingCases extends Component {
    constructor(props) {
        super(props);
        this.state = {
            case_list: null
        };
    }
    componentDidMount() {
        axios.get("/api/getPendingCase")
            .then(res => {
                if (res.data.confirm == "0") {
                    alert(res.data.message);                    
                }
                else {
                    this.setState({
                        case_list: res.data.case_list.map((item) => {
                            return (
                                {
                                    'cin': item.cin,
                                    'def_name': item.def_name,
                                    'def_addr': item.def_addr,
                                    'crime_type': item.crime_type,
                                    'crime_date': new Date(parseInt(item.crime_date.year), parseInt(item.crime_date.month) - 1, parseInt(item.crime_date.day)),
                                    'crime_loc': item.crime_loc,
                                    'arresting_off_name': item.arresting_off_name,
                                    'arrest_date': new Date(parseInt(item.arrest_date.year), parseInt(item.arrest_date.month) - 1, parseInt(item.arrest_date.day)),
                                    'name_pres_judge': item.name_pres_judge,
                                    'public_prosecutor_name': item.public_prosecutor_name,
                                    'arrest_date': new Date(parseInt(item.starting_date.year), parseInt(item.starting_date.month) - 1, parseInt(item.starting_date.day))
                                }
                            );

                        })
                    }, () => console.log('Get Pending :', this.state.case_list));
                }

            })
            .catch(err => {
                err.response ? alert('Error in Server ' + err.response.status) : console.log(err);
            });
    }
    render() {
        return (<Router>
            <div className="Registrar">
                <div className="Registrar-header">
                    {
                        this.props.goback ?
                            <button
                                onClick={this.props.goback}
                                style={{ marginLeft: "auto" }}
                                className="btn btn-primary "
                            >
                                Go Back
                            </button>
                            : null
                    }

                    <h4>Pending Cases: </h4>
                    <div className="ag-theme-balham-dark" style={{ height: 400, width: 1000 }}>
                        <AgGridReact
                            rowData={this.state.case_list}>
                            <AgGridColumn onCellClicked={this.props.handleselect ? this.props.handleselect : null} field="cin" sortable="true"></AgGridColumn>
                            <AgGridColumn field="def_name"></AgGridColumn>
                            <AgGridColumn field="def_addr"></AgGridColumn>
                            <AgGridColumn field="crime_type"></AgGridColumn>
                            <AgGridColumn field="crime_date"></AgGridColumn>
                            <AgGridColumn field="crime_loc"></AgGridColumn>
                            <AgGridColumn field="arresting_off_name"></AgGridColumn>
                            <AgGridColumn field="arrest_date"></AgGridColumn>
                            <AgGridColumn field="name_pres_judge"></AgGridColumn>
                            <AgGridColumn field="public_prosecutor_name"></AgGridColumn>
                            <AgGridColumn field="arrest_date"></AgGridColumn>
                        </AgGridReact>
                    </div>
                </div>
            </div>
        </Router>
        );

    }
}