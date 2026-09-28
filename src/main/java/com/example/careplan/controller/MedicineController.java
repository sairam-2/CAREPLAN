package com.example.careplan.controller;

import com.example.careplan.dto.AddMedicineRequest;
import com.example.careplan.dto.MedicineResponse;
import com.example.careplan.service.MedicineService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/medicines")
public class MedicineController {

    private final MedicineService medicineService;

    public MedicineController(MedicineService medicineService) {
        this.medicineService = medicineService;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public MedicineResponse addMedicine(@Valid @RequestBody AddMedicineRequest request) {
        return medicineService.addMedicine(request);
    }
}
