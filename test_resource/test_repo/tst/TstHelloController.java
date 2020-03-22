package com.boraji.tutorial.springboot.controller;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.ss.usermodel.WorkbookFactory;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController

public class HelloController {

public void Test_AddMethod() {  
            BasicMaths bm = new BasicMaths();  
            double res = bm.Add(1, 10);  
            Assert.AreEqual(res, 5);  
        } 
public void Test_AddMethod() {  
            BasicMaths bm = new BasicMaths();  
            double res = bm.Add(10, 10);  
            Assert.AreEqual(res, 2);  
        } 
 


}
