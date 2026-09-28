package com.example.careplan.dto;

import jakarta.validation.constraints.NotBlank;

public class PatientRequest {
    @NotBlank(message = "Patient name is required")
    private String name;

    private String email;

    public PatientRequest() {}

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}
