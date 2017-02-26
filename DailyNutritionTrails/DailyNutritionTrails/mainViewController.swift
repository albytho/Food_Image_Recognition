//
//  mainViewController.swift
//  DailyNutritionTrails
//
//  Created by Alby Thomas on 2/26/17.
//  Copyright © 2017 Microsoft. All rights reserved.
//

import UIKit

var objects: [String] = []

class mainViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate,AnalyzeImageDelegate{
    
    @IBOutlet var Label: UITextField!
    
    @IBAction func button_click(_ sender: Any) {
        imagePicker =  UIImagePickerController()
        imagePicker.delegate = self
        imagePicker.sourceType = .camera
        
        present(imagePicker, animated: true, completion: nil)
    }
    
    func finnishedGeneratingObject(_ analyzeImageObject: AnalyzeImage.AnalyzeImageObject) {
        
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        Label.text = " "
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
        
        imagePicker.dismiss(animated: true, completion: nil)
        
        
        let image = info["UIImagePickerControllerOriginalImage"] as! UIImage
        
        let analyzeImage = CognitiveServices.sharedInstance.analyzeImage
        analyzeImage.delegate = self
        
        let visualFeatures: [AnalyzeImage.AnalyzeImageVisualFeatures] = [.Categories, .Description, .Faces, .ImageType, .Color, .Adult]
        let requestObject: AnalyzeImageRequestObject = (image, visualFeatures)
        
        try! analyzeImage.analyzeImageWithRequestObject(requestObject, completion: { (response) in
            DispatchQueue.main.async(execute: {
                print(response!.tags![0])
                //self.Label.text = "\response!.tags![0]"
                //objects.append(response!.tags![0])
                
            })
        })
        
    }
    
    var imagePicker: UIImagePickerController!
    
    
    /*
     // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
