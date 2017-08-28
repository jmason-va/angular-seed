import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'workout-component',
  template: `
  <div class="container">
  
      <md-card class="exercise" *ngFor="let exercise of exercises">
        <div *ngIf="exercise.movement" class="movement"> {{exercise.movement}}</div>
        <span class="label">{{exercise.date | date}} </span>
        <span *ngIf="exercise.weight">{{exercise.weight}}</span>
        <span class="label">lbs</span>
        <span *ngIf="exercise.reps">{{exercise.reps}} </span>
        <span class="label">reps</span>
        <span *ngIf="exercise.sets">{{exercise.sets}} </span>
        <span class="label">sets</span>
        <button (click)="removeExercise(exercise)"> x </button>
      </md-card>
  
      <md-card (keydown)="keyDownFunction($event, focusable)" class="add-exercise">
        <div class="row">
          <div class="col col-xs-9">
            <md-input-container> <input mdInput placeholder="movement" #focusable [(ngModel)]="movement"></md-input-container>
            <md-input-container> <input mdInput placeholder="weight" [(ngModel)]="weight"></md-input-container>
            <md-input-container> <input mdInput placeholder="sets" [(ngModel)]="sets"></md-input-container>
            <md-input-container> <input mdInput placeholder="reps" [(ngModel)]="reps"></md-input-container>
          </div>
          <div class="col col-xs-3">
            <button style="float: right " md-button (click)="addExercise()">+</button>
          </div>
        </div>
      </md-card>
  
      
    </div>
  `,
  styles: [`
    .container {
      margin: auto;
      width: 800px;
    }

    md-card {
      margin: 10px 0;
    }
    
    input {
      width: 130px;
    }

    .movement {
      display: inline-flex;
      width: 100px;
      color: #66d9ef;
    }
    
    .title {
      color: #66d9ef; 
    }
    .sets {
      color: #66d9ef;
    }
    .label {
      color: #8c8c8c;
      font-size: 10px;
      padding-right: 5px;
    }
    .pb {
      color: #e6db74;
    }
  `]
})
export class WorkoutComponent implements OnInit {
  movement;
  weight;
  sets;
  reps;
  
  constructor() { }
  ngOnInit() {}

  
  addExercise() {
    this.exercises.push({
      movement: this.movement,
      weight: this.weight,
      sets: this.sets,
      reps: this.reps,
      date: Date.now()
    });
    this.clearInputs();
  }

  removeExercise(exercise) {
    let index = this.exercises.indexOf(exercise);
    this.exercises.splice(index, 1);
  }

  clearInputs() {
    this.movement = null;
    this.weight = null;
    this.sets = null;
    this.reps = null;
  }

  keyDownFunction(event, el) {
    if (event.keyCode == 13) {
      el.focus();
      this.addExercise(); 
    }
  }

  private EXERCISES = [
    {
      movement: 'bench press',
      weight: 200,
      sets: 3,
      reps: 10, 
      date: Date.now()
    },
    { 
      movement: 'squat',
      weight: 155,
      sets: 3,
      reps: 10,
      date: Date.now()
    },
  ];

  get exercises(){
    return this.EXERCISES;
  }

}
