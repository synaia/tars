/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { loadBundle } from "@web/core/assets";
import { registry } from "@web/core/registry";
import { formatFloat } from "@web/views/fields/formatters";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

import { Component, onWillStart, useEffect, useRef } from "@odoo/owl";

export class CustomAudioPlayer extends Component {
    setup() {
        this.chart = null;
        this.waveSurferRef = useRef({
            isPlaying: () => false,
          })
        this.audioContainer = useRef("audio_container");
        this.playButton = useRef("audio_play");

        onWillStart(async () => await loadBundle("web.wavesurfer"));

        useEffect(() => {
            const audoo_path = this.props.record.data[this.props.name] || "https://s3-us-west-2.amazonaws.com/s.cdpn.io/86186/First_To_Last.mp3";
            const waveSurfer = WaveSurfer.create({
                container: this.audioContainer.el,
                height: 70,
                waveColor: '#ECF2FF',
                progressColor: '#71639e',
                barWidth: 5,
                barGap: 2,
                barRadius: 10,
                cursorColor: '#787186',
                cursorWidth: 1,
                responsive: true,
                // plugins: [TimelinePlugin.create({
                //   height: 17,
                // })],
            });
            waveSurfer.load(audoo_path);

            const clickPlay = (el) => {
                waveSurfer.playPause();
                el.target.innerHTML = waveSurfer.isPlaying() ? "Pause" : "Play";
            }

            waveSurfer.on('ready', () => {
                console.log(waveSurfer)
            });

            this.playButton.el.addEventListener("click", clickPlay)

            return () => {
                waveSurfer.destroy()
                this.playButton.el.removeEventListener("click", clickPlay)
            };
        });
    }

   

}

CustomAudioPlayer.template = "web.CustomAudioPlayer";
CustomAudioPlayer.props = {
    ...standardFieldProps,
};

export const audioPlayer = {
    component: CustomAudioPlayer,
    // extractProps: ({ options }) => ({
    //     title: options.title,
    //     maxValue: options.maxValue || 9, // Extract maxValue or use default 9
    //     score: options.score || 0,
    //     backgroundColor: options.backgroundColor || "#1f77b4", // Extract backgroundColor or use default color
    // }),
};

registry.category("fields").add("custom_audio_player", audioPlayer);
