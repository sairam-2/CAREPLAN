package com.example.careplan.dto;

import java.time.LocalTime;
import java.util.List;

public class MedicineResponse {
    private Long id;
    private Long patientId;
    private String name;
    private String dosage;
    private String frequency;
    private List<LocalTime> timings;

    public MedicineResponse(Long id, Long patientId, String name, String dosage, String frequency, List<LocalTime> timings) {
        this.id = id;
        this.patientId = patientId;
        this.name = name;
        this.dosage = dosage;
        this.frequency = frequency;
        this.timings = timings;
    }

    public Long getId() { return id; }
    public Long getPatientId() { return patientId; }
    public String getName() { return name; }
    public String getDosage() { return dosage; }
    public String getFrequency() { return frequency; }
    public List<LocalTime> getTimings() { return timings; }
}
