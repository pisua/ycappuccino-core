import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { appRoutes } from './app.routes';

import { HeaderComponent } from './partials/header/header.component';
import { MatchDetailComponent } from './resources/matches/match-detail/match-detail.component';
import { MatchListComponent } from './resources/matches/match-list/match-list.component';
imports: [BrowserModule, RouterModule.forRoot(appRoutes)]

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    MatchDetailComponent,
    MatchListComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
