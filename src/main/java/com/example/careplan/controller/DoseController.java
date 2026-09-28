package com.example.careplan.controller;

import com.example.careplan.dto.DoseLogRequest;
import com.example.careplan.dto.DoseLogResponse;
import com.example.careplan.dto.DoseResponse;
import com.example.careplan.dto.MissedDoseResponse;
import com.example.careplan.service.DoseService;
import jakarta.validation.Valid;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping("/api/doses")
public class DoseController {

    private final DoseService doseService;

    public DoseController(DoseService doseService) {
        this.doseService = doseService;
    }

    @GetMapping("/today/patient/{patientId}")
    public List<DoseResponse> getExpectedDosesForToday(@PathVariable Long patientId) {
        return doseService.getExpectedDosesForToday(patientId);
    }

    @PostMapping("/log")
    public DoseLogResponse logDose(@Valid @RequestBody DoseLogRequest request) {
        return doseService.logDose(request);
    }

    @GetMapping("/missed/patient/{patientId}")
    public List<MissedDoseResponse> getMissedDoses(
            @PathVariable Long patientId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {
        return doseService.getMissedDoses(patientId, startDate, endDate);
    }
}
