import 'dart:convert'; // For base64 encoding
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io' as io; // For handling images on mobile
import 'dart:html' as html; // For web image handling
import 'package:flutter/foundation.dart'; // For kIsWeb
import 'package:http/http.dart' as http; // For making API requests

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() {
    return _HomeScreenState();
  }
}

class _HomeScreenState extends State<HomeScreen> {
  String? _webImage; // Store base64 string for web
  io.File? _mobileImage; // Store image file for mobile
  final ImagePicker _picker = ImagePicker(); // Image picker instance
  final TextEditingController _textController = TextEditingController(); // Text input controller
  String? _processedImage; // Store processed image from server
  bool _isLoading = false; // Loading state

  // Function to pick an image from the gallery
  Future<void> _pickImageFromGallery() async {
    final pickedFile = await _picker.pickImage(source: ImageSource.gallery);
    if (pickedFile != null) {
      await _processImage(pickedFile);
    }
  }

  // Function to capture an image using the camera
  Future<void> _pickImageFromCamera() async {
    final pickedFile = await _picker.pickImage(source: ImageSource.camera);
    if (pickedFile != null) {
      await _processImage(pickedFile);
    }
  }

  // Function to handle both mobile and web image selection
  Future<void> _processImage(XFile pickedFile) async {
    try {
      if (kIsWeb) {
        // Web: Convert to Base64 string
        final bytes = await pickedFile.readAsBytes();
        final reader = html.FileReader();

        reader.onLoadEnd.listen((event) {
          setState(() {
            _webImage = reader.result as String?;
            _mobileImage = null; // Clear mobile image
          });
        });

        reader.readAsDataUrl(html.File([bytes], pickedFile.name));
      } else {
        // Mobile: Use File directly
        setState(() {
          _mobileImage = io.File(pickedFile.path);
          _webImage = null; // Clear web image
        });
      }
    } catch (e) {
      print('Error processing image: $e');
    }
  }

  // Function to call Flask API and send image & text
  Future<void> _sendImageAndTextToAPI() async {
    if ((_mobileImage == null && _webImage == null) || _textController.text.isEmpty) {
      // If no image or text is provided, show a warning
      print("Please provide both an image and text.");
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      // Convert the image to base64
      String base64Image;
      if (kIsWeb) {
        base64Image = _webImage!.split(',')[1]; // For web, extract base64 data only
      } else {
        final bytes = await _mobileImage!.readAsBytes();
        base64Image = base64Encode(bytes);
      }

      // Prepare the API request payload
      final response = await http.post(
        Uri.parse('http://127.0.0.1:5000/process_image'), // Flask API endpoint
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'image': 'data:image/png;base64,$base64Image',
          'text': _textController.text,
        }),
      );

      if (response.statusCode == 200) {
        // If successful, get the processed image from the response
        final responseData = jsonDecode(response.body);
        setState(() {
          _processedImage = responseData['result_image'];
          _isLoading = false;
        });
      } else {
        print('Error: ${response.body}');
        setState(() {
          _isLoading = false;
        });
      }
    } catch (e) {
      print('Error calling API: $e');
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0),
            child: TextField(
              controller: _textController,
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Enter some text',
                hintText: 'Type here...',
                filled: true,
                fillColor: Colors.white,
              ),
            ),
          ),
          const SizedBox(height: 20),
          Container(
            width: 300,
            height: 300,
            decoration: BoxDecoration(
              border: Border.all(color: Colors.grey),
            ),
            child: _processedImage != null
                ? Image.network(
                    _processedImage!,
                    fit: BoxFit.cover,
                    errorBuilder: (context, error, stackTrace) {
                      return const Center(
                        child: Text(
                          'Failed to load image',
                          style: TextStyle(color: Colors.red),
                        ),
                      );
                    },
                  )
                : _webImage != null
                    ? Image.network(
                        _webImage!,
                        fit: BoxFit.cover,
                        errorBuilder: (context, error, stackTrace) {
                          return const Center(
                            child: Text(
                              'Failed to load image',
                              style: TextStyle(color: Colors.red),
                            ),
                          );
                        },
                      )
                    : _mobileImage != null
                        ? Image.file(
                            _mobileImage!,
                            fit: BoxFit.cover,
                            errorBuilder: (context, error, stackTrace) {
                              return const Center(
                                child: Text(
                                  'Failed to load image',
                                  style: TextStyle(color: Colors.red),
                                ),
                              );
                            },
                          )
                        : Image.asset(
                            'assets/image.png', // Placeholder image
                            fit: BoxFit.cover,
                          ),
          ),
          const SizedBox(height: 20),
          ElevatedButton.icon(
            onPressed: _pickImageFromGallery,
            icon: const Icon(Icons.photo),
            label: const Text('Pick from Gallery'),
          ),
          const SizedBox(height: 10),
          ElevatedButton.icon(
            onPressed: _pickImageFromCamera,
            icon: const Icon(Icons.camera_alt),
            label: const Text('Capture from Camera'),
          ),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: _isLoading ? null : _sendImageAndTextToAPI,
            child: _isLoading
                ? const CircularProgressIndicator()
                : const Text('Submit Image and Text'),
          ),
        ],
      ),
    );
  }
}
