//Ref: https://blog.logrocket.com/complete-guide-building-smart-data-table-react/

import React from "react";
import { useTable } from "react-table";

export default function Table({ columns, data }) {

    return (
        <table>
            <tr>
                {columns.map((value, index) => {
                    return (<th>{value.Header}</th>)
                })}
            </tr>
            {data.map((value,index)=>{
                return <tr>{columns.map((val,ind)=>{
                    return <td>{value[val.accessor]}</td>
                })}</tr>
            })}

        </table>
    )
}