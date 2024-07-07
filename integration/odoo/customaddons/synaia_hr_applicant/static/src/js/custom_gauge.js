/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { loadBundle } from "@web/core/assets";
import { registry } from "@web/core/registry";
import { formatFloat } from "@web/views/fields/formatters";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

import { Component, onWillStart, useEffect, useRef } from "@odoo/owl";

export class GaugeField extends Component {
    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");

        onWillStart(async () => await loadBundle("web.chartjs_lib"));

        useEffect(() => {
            this.renderChart();
            return () => {
                if (this.chart) {
                    this.chart.destroy();
                }
            };
        });
    }

    get title() {
        return this.props.title || this.props.record.fields[this.props.name].string || "";
    }

    get formattedValue() {
        return formatFloat(this.props.record.data[this.props.name], {
            humanReadable: true,
            decimals: 1,
        });
    }

    get strokeColor() {
        const gaugeValue = this.props.record.data[this.props.name];
        if (gaugeValue > 0.6) {
            return "#ff0000"; // Red
        } else if (gaugeValue >= 0.5) {
            return "#ffa500"; // Orange
        } else {
            return "#ffff00"; // Yellow
        }
    }

    renderChart() {
        const gaugeValue = this.props.record.data[this.props.name];
        let maxValue = 1; // Maximum value is always 1
        let maxLabel = maxValue;
        if (gaugeValue === 0 && maxValue === 0) {
            maxValue = 1;
            maxLabel = 0;
        }
        const config = {
            type: "doughnut",
            data: {
                datasets: [
                    {
                        data: [gaugeValue, maxValue - gaugeValue],
                        backgroundColor: [this.strokeColor, "#dddddd"],
                        label: this.title,
                    },
                ],
            },
            options: {
                circumference: 180,
                rotation: 270,
                responsive: true,
                maintainAspectRatio: false,
                cutout: "70%",
                layout: {
                    padding: 5,
                },
                plugins: {
                    title: {
                        display: true,
                        text: this.title,
                        padding: 4,
                    },
                    tooltip: {
                        displayColors: false,
                        callbacks: {
                            label: function (tooltipItem) {
                                if (tooltipItem.dataIndex === 0) {
                                    return _t("Value: ") + gaugeValue;
                                }
                                return _t("Max: ") + maxLabel;
                            },
                        },
                    },
                    // Adding the label in the center of the gauge
                    datalabels: {
                        display: true,
                        formatter: (value, context) => {
                            return context.dataIndex === 0 ? 'gaugeValue' : '';
                        },
                        color: "#000",
                        font: {
                            size: 20,
                            weight: 'bold',
                        },
                    },
                },
                aspectRatio: 2,
            },
        };
        this.chart = new Chart(this.canvasRef.el, config);

        // Add needle indicator
        this.addNeedle(gaugeValue);
    }

    addNeedle(value) {
        const ctx = this.canvasRef.el.getContext('2d');
        const angle = (1 - value) * Math.PI; // Convert value to angle
        const radius = (this.canvasRef.el.width / 2) * 0.9; // Needle radius
        const centerX = this.canvasRef.el.width / 2;
        const centerY = this.canvasRef.el.height - 10; // Adjust for better alignment

        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.rotate(angle);
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(0, -radius);
        ctx.lineWidth = 2;
        ctx.strokeStyle = "#000";
        ctx.stroke();
        ctx.restore();
    }
}

GaugeField.template = "web.CustomGaugeField";
GaugeField.props = {
    ...standardFieldProps,
    maxValueField: { type: String },
    title: { type: String, optional: true },
    label_field: { type: String, optional: true }, 
};

export const gaugeField = {
    component: GaugeField,
    supportedOptions: [
        {
            label: _t("Title"),
            name: "title",
            type: "string",
        },
        {
            label: _t("Max value field"),
            name: "max_value",
            type: "field",
            availableTypes: ["integer", "float"],
        },
        {
            label: _t("label value field"),
            name: "label_field",
            type: "string",
        },
    ],
    extractProps: ({ options }) => ({
        maxValueField: options.max_field,
        title: options.title,
        label_field: options.label_field,
    }),
};

registry.category("fields").add("custom_gauge", gaugeField);
