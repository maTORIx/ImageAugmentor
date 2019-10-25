
const API_ROOT = "/api"
const DEFAULT_AUGMENT_OPTIONS = ["crop", "crop", "flip-horizontal", "flip-vertical"]

document.addEventListener("DOMContentLoaded", function() {
    let app = new Vue({
        el: "#app",
        data() {
            return {
                datasets: [],
                results: [],
                selected_dataset: null,
                selected_augment_options: [],
                augment_option_choises: {},
                augment_option_dialog: false,
                augment_sample_data: [],
                augment_sample_loading: false,
                augment_sample_dialog: false,
                error: []
            }
        },
        methods: {
            async loadDatasets(ids=[]) {
                const target = API_ROOT + "/datasets"
                if (ids.length > 0) target += "?ids=" + ids.join(",")
                
                const res = await fetch(target)
                if (!res.ok) throw new Error("Failed to access api.")
                return res.json()
            },
            async loadResults(ids=[]) {
                const target = API_ROOT + "/results"
                if (ids.length > 0) target += "?ids=" + ids.join(",")
                
                const res = await fetch(target)
                if (!res.ok) throw new Error("Failed to access api.")
                return res.json()
            },
            async loadAugmentOptionChoises() {
                const target = API_ROOT + "/augment/option_choises"
                const res = await fetch(target)
                if (!res.ok) throw new Error("Failed to access api.")
                return res.json()
            },
            createError(err) {
                console.error(err)
                this.error.push(err.toString())
            },
            selectDataset(id) {
                this.selected_dataset = id
            },
            addAugmentOption(option_name) {
                if (!Object.keys(this.augment_option_choises).includes(option_name)) {
                    this.createError(new Error("Invalid option. Augment option doesn't include this option."))
                }
                this.selected_augment_options.push(option_name)
            },
            toggleAugmentOptionDialog() {
                const augment_option_dialog = document.querySelector("#augment-choises-dialog")
                this.augment_option_dialog = !this.augment_option_dialog
                if (this.augment_option_dialog) {
                    augment_option_dialog.showModal()
                } else {
                    augment_option_dialog.close()
                }
            },
            toggleAugmentSampleDialog() {
                const augment_sample_dialog = document.querySelector("#augment-sample-dialog")
                this.augment_sample_dialog = !this.augment_sample_dialog
                if (this.augment_sample_dialog) {
                    augment_sample_dialog.showModal()
                } else {
                    augment_sample_dialog.close()
                }
            }
        },
        async mounted() {
            try {
                [this.datasets, this.results, this.augment_option_choises] = await Promise.all([
                    this.loadDatasets(),
                    this.loadResults(),
                    this.loadAugmentOptionChoises()
                ])
                this.selected_augment_options = DEFAULT_AUGMENT_OPTIONS
                console.log(await this.augment_option_choises)
            } catch(e) {
                this.error.push(e.toString())
            }
        }
    })
})