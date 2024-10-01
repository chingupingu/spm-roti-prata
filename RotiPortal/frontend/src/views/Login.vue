<script setup>

</script>

<template>

    <div class="container-fluid">
        <form @submit.prevent="authenticate()">
            <!-- Login form -->
            <div class="row justify-content-center my-3">
                <div style="width: 400px;" class="bg-light rounded-3 p-3">
                    <h1 class="text-center">Login</h1>
                    <div class="mb-3">
                        <label for="email" class="form-label">Email:</label>
                        <input required v-model="email" type="text" class="form-control" id="email">
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password:</label>
                        <input required v-model="password" type="password" class="form-control" id="password"
                            placeholder="">
                    </div>
                    <div class="mb-3">
                        <p class="text-danger">{{ errorMsg }}</p>
                    </div>
                    <div class="mb-2 mt-4 text-center">
                        <button type="submit" class="btn btn-primary">Login</button>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'login',
    data() {
        return {
            email: '',
            password: '',
            errorMsg: '',
        }
    },
    methods: {
        async authenticate() {
            this.errorMsg = ""
            
            // Check if email exists
            try {
                const response = await axios.post("http://localhost:5000/employee/login", { email: this.email })
                if (response.data) {
                    // Continue with authentication if email exists
                    if (this.password == "0000") {
                        sessionStorage.setItem("employee_obj", JSON.stringify(response.data))
                        this.redirect()
                        // if (response.data.Role == "Staff") {
                        //     sessionStorage.setItem("user", "staff")
                        // } else if (address == "manager.rp.com") {
                        //     sessionStorage.setItem("user", "manager")
                        //     this.redirect()
                        // } else if(address == "hr.rp.com") {
                        //     sessionStorage.setItem("user", "hr")
                        //     this.redirect()
                        // } else {
                        //     this.errorMsg = "Invalid email domain."
                        // }
                    } else {
                        this.errorMsg = "Your password is incorrect."
                    }
                } else {
                    this.errorMsg = "This user does not exist."
                    return
                }
            } catch (error) {
                console.error("Error checking email:", error)
                this.errorMsg = "An error occurred while checking the email."
                return
            }

        },


        redirect() {
            this.$router.push({ path: `/home`, replace: true })
        }

    },
    mounted() {
        sessionStorage.clear()
    }
}
</script>