package com.example.careplan.service;

import com.example.careplan.dto.AddMedicineRequest;
import com.example.careplan.dto.MedicineResponse;
import com.example.careplan.entity.Medicine;
import com.example.careplan.entity.Patient;
import com.example.careplan.entity.Schedule;
import com.example.careplan.exception.ResourceNotFoundException;
import com.example.careplan.repository.MedicineRepository;
import com.example.careplan.repository.PatientRepository;
import com.example.careplan.repository.ScheduleRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

@Service
public class MedicineService {

    private final MedicineRepository medicineRepository;
    private final PatientRepository patientRepository;
    private final ScheduleRepository scheduleRepository;

    public MedicineService(MedicineRepository medicineRepository, PatientRepository patientRepository, ScheduleRepository scheduleRepository) {
        this.medicineRepository = medicineRepository;
        this.patientRepository = patientRepository;
        this.scheduleRepository = scheduleRepository;
    }

    @Transactional
    public MedicineResponse addMedicine(AddMedicineRequest request) {
        Patient patient = patientRepository.findById(request.getPatientId())
                .orElseThrow(() -> new ResourceNotFoundException("Patient not found with ID: " + request.getPatientId()));

        Medicine medicine = new Medicine();
        medicine.setPatient(patient);
        medicine.setName(request.getName());
        medicine.setDosage(request.getDosage());
        medicine.setFrequency(request.getFrequency());

        Medicine savedMedicine = medicineRepository.save(medicine);
        List<LocalTime> savedTimings = new ArrayList<>();

        for (LocalTime time : request.getTimings()) {
            Schedule schedule = new Schedule();
            schedule.setExpectedTime(time);
            schedule.setMedicine(savedMedicine);
            scheduleRepository.save(schedule);
            savedTimings.add(time);
        }

        return new MedicineResponse(savedMedicine.getId(), patient.getId(), savedMedicine.getName(), savedMedicine.getDosage(), savedMedicine.getFrequency(), savedTimings);
    }
}
