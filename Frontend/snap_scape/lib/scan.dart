import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:snap_scape/home.dart';
import 'package:snap_scape/start_screen.dart';

class Scan extends StatefulWidget {
 Scan({super.key});

  @override
  State<Scan> createState()
  {
    return _ScanState();
  }
}

class _ScanState extends State<Scan>{

  Widget? activeScreen;

  @override
  void initState() {
    
    activeScreen = StartScreen(switchScreen);

    super.initState();
  }

  void switchScreen()
  {
    setState(() {
      activeScreen = HomeScreen();
    });
  }

  @override
   Widget build(context)
   {
    return MaterialApp(
      home: Scaffold(
    body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [
              Color.fromARGB(255, 11, 125, 219),
              Color.fromARGB(255, 28, 63, 179),
            ],
            begin: Alignment.topLeft, 
          end: Alignment.bottomRight)),
           child: activeScreen),
          ),
        );
   }
}