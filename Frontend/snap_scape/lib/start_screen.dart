import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'dart:async';

class StartScreen extends StatelessWidget {
  const StartScreen(this.startApp,{super.key});

  final void Function() startApp;

   void DelayedswitchScreen() {
    Timer(const Duration(seconds: 2), startApp);
  }

  @override
  Widget build(context) {
      DelayedswitchScreen();
    return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
      children: [Image.asset('assets/logo.png'),
      const SpinKitRing(
  color: Colors.white,
  size: 50.0,
),
],
    ));
  }
}
