import 'package:flutter/material.dart';
import 'constants.dart';

class MenuItem extends StatelessWidget {
  final String title;
  final Function press;
  const MenuItem({ Key? key, required this.title, required this.press, }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: (){
        press();
      },
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 15),
        child: Text(
          title.toUpperCase(),
          style: TextStyle(color: kDarkBlueColorT1.withOpacity(0.3), fontWeight: FontWeight.bold),
        ),
      ),
    );
    
  }
}