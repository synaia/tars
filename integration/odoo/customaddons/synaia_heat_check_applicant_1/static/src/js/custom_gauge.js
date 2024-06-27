/** @odoo-module */

import { registry } from "@web/core/registry";
import { Component, useRef, useEffect, onMounted, onRendered, onPatched } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class CustomGauge extends Component {
    static props = { 
        ...standardFieldProps,
        leadHeatCheck: { type: String, optional: true },
     };
    static template = 'synaia_heat_check_applicant_1.GaugeFieldTemplate';
    
    setup() {
        super.setup();
        this.canvasRef = useRef('gaugeCanvas');
        console.log("***** Estoy contento!!! ", this.props)

        onMounted(() => {
            this.renderGauge();
        });
    }

    renderGauge() {
        console.log("**** renderGauge() ", this.props.record.data.lead_temperature)

        const value = this.props.record.data[this.props.name] || 0;
        const lead_heat_check_label = this.props.record.data.lead_heat_check || 'Not Defined';
        // this.props.record.data[this.props.leadHeatCheck]
        const canvas = this.canvasRef.el;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        const gaugeValue = Math.min(1.0, Math.max(0.0, value));

        // Clear the canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw the background half-circle
        ctx.beginPath();
        ctx.arc(100, 100, 90, Math.PI, 0);
        ctx.strokeStyle = '#eee';
        ctx.lineWidth = 10;
        ctx.stroke();

        // Determine the color based on the value
        let strokeColor;
        if (gaugeValue > 0.6) {
            strokeColor = '#FF0000'; // Red
        } else if (gaugeValue >= 0.5) {
            strokeColor = '#FCA946'; // Orange
        } else {
            strokeColor = '#FCF146'; // Yellow
        }

        // Draw the gauge value
        const startAngle = Math.PI;
        const endAngle = startAngle + (Math.PI * gaugeValue);
        ctx.beginPath();
        ctx.arc(100, 100, 90, startAngle, endAngle);
        ctx.strokeStyle = strokeColor;
        ctx.lineWidth = 10;
        ctx.stroke();

        // Draw the label text
        ctx.fillStyle = '#000';
        ctx.font = '20px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(lead_heat_check_label, 100, 80);

        // Draw the percentage value
        ctx.font = '30px Arial';
        ctx.fillText(`${gaugeValue}`, 100, 120);
    }
}

export const customGauge = {
    component: CustomGauge,
    extractProps: ({ options }) => ({
        leadHeatCheck: options.lead_heat_check_label,
    }),
    supportedTypes: ["float"],
};

registry.category("fields").add("custom_gauge", customGauge);